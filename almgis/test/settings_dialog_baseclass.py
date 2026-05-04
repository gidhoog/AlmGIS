import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

from PyQt5.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QCheckBox, QSpinBox, QFormLayout,
    QFrame, QDialog, QTreeWidget, QTreeWidgetItem, QStackedWidget,
    QDialogButtonBox, QSplitter, QComboBox
)
from qgis.PyQt.QtCore import Qt, QSettings, QSize
from qgis.PyQt.QtGui import QIcon
from qgis.gui import QgsOptionsPageWidget


# ── 1. Registry ──────────────────────────────────────────────────────────────

@dataclass
class SettingsPageDescriptor:
    """
    Describes a single settings page entry.

    Attributes
    ----------
    title    : Label shown in the tree.
    factory  : Zero-argument callable that returns a QgsOptionsPageWidget.
    group    : Optional group name. Pages sharing the same group are
               placed under the same tree parent node.
    icon     : QIcon for the tree item (defaults to empty icon).
    tooltip  : Tooltip shown on the tree item.
    order    : Lower values sort first within the same group.
    """
    title:   str
    factory: Callable[[], QgsOptionsPageWidget]
    group:   Optional[str]            = None
    icon:    QIcon                    = field(default_factory=QIcon)
    tooltip: str                      = ""
    order:   int                      = 100


class SettingsPageRegistry:
    """
    Central registry for settings page descriptors.

    Usage
    -----
    # Register a page (typically at module / app startup)
    SettingsPageRegistry.register(SettingsPageDescriptor(
        title   = "Network",
        factory = NetworkSettingsPage,
        group   = "Advanced",
        icon    = QIcon.fromTheme("network-workgroup"),
        tooltip = "Proxy and connection settings",
        order   = 10,
    ))

    # The dialog calls this to get all registered descriptors
    SettingsPageRegistry.pages()
    """

    _descriptors: list[SettingsPageDescriptor] = []

    @classmethod
    def register(cls, descriptor: SettingsPageDescriptor) -> None:
        """Register a settings page descriptor."""
        cls._descriptors.append(descriptor)

    @classmethod
    def pages(cls) -> list[SettingsPageDescriptor]:
        """
        Return all registered descriptors sorted by group, then order,
        then title.
        """
        return sorted(
            cls._descriptors,
            key=lambda d: (d.group or "", d.order, d.title),
        )

    @classmethod
    def clear(cls) -> None:
        """Remove all registered descriptors (useful in tests)."""
        cls._descriptors.clear()


# ── 2. Base settings dialog ──────────────────────────────────────────────────

class BaseSettingsDialog(QDialog):
    """
    Base settings dialog with a QTreeWidget on the left and a
    QStackedWidget on the right.

    It reads from SettingsPageRegistry at construction time, so any pages
    registered before exec() is called will appear automatically.

    Subclass this to add app-specific behaviour (custom stylesheet,
    extra buttons, etc.) without touching the page registration logic.

    Example
    -------
    class MyAppSettingsDialog(BaseSettingsDialog):
        def __init__(self, parent=None):
            super().__init__(parent, title="My App – Settings")
    """

    _GROUP_ROLE = Qt.UserRole + 1   # marks group (non-page) tree items

    def __init__(self, parent=None, *, title: str = "Settings"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(780, 560)
        self.setMinimumSize(640, 420)

        # live instances created from descriptors
        self._pages: list[QgsOptionsPageWidget] = []

        # id(QTreeWidgetItem) → stack index
        # QTreeWidgetItem is not hashable in PyQt, so we use id() of the
        # object (its memory address) as the dict key instead.
        # This is safe because all items are owned by the QTreeWidget and
        # live for the entire lifetime of the dialog.
        self._page_index: dict[int, int] = {}

        self._build_ui()
        self._populate_from_registry()
        self._apply_stylesheet()
        self._select_first_leaf()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)   # ← was (0, 0, 0, 8)
        root.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)

        # ── Left panel ───────────────────────────────────────────────────────
        left = QWidget()
        left.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("searchEdit")
        self.search_edit.setPlaceholderText("🔍  Search settings…")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._filter_tree)
        left_layout.addWidget(self.search_edit)

        self.tree = QTreeWidget()
        self.tree.setObjectName("optionsTree")
        self.tree.setHeaderHidden(True)
        self.tree.setIconSize(QSize(20, 20))
        self.tree.setIndentation(16)
        self.tree.setAnimated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.tree.currentItemChanged.connect(self._on_item_changed)
        left_layout.addWidget(self.tree)

        self.splitter.addWidget(left)

        # ── Right panel ──────────────────────────────────────────────────────
        right = QWidget()
        right.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Title bar
        self.page_title_bar = QWidget()
        self.page_title_bar.setObjectName("pageTitleBar")
        self.page_title_bar.setFixedHeight(46)
        title_bar_layout = QHBoxLayout(self.page_title_bar)
        title_bar_layout.setContentsMargins(16, 0, 16, 0)

        self.page_icon_label = QLabel()
        self.page_icon_label.setFixedSize(22, 22)
        title_bar_layout.addWidget(self.page_icon_label)

        self.page_title_label = QLabel()
        self.page_title_label.setObjectName("pageTitleLabel")
        title_bar_layout.addWidget(self.page_title_label)
        title_bar_layout.addStretch()

        right_layout.addWidget(self.page_title_bar)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("titleSeparator")
        right_layout.addWidget(sep)

        self.stack = QStackedWidget()
        self.stack.setObjectName("optionsStack")
        right_layout.addWidget(self.stack)

        self.splitter.addWidget(right)
        self.splitter.setSizes([210, 570])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        root.addWidget(self.splitter)

        # ── Button box ───────────────────────────────────────────────────────
        btn_frame = QFrame()
        btn_frame.setObjectName("buttonFrame")
        btn_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # ← no vertical stretch

        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(8, 4, 8, 4)   # ← tight equal margins all round

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self._apply_all)
        btn_layout.addWidget(self.button_box)

        root.addWidget(btn_frame)

    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QDialog { background: #f5f5f5; }
            QWidget#leftPanel {
                background: #e8e8e8;
                border-right: 1px solid #c8c8c8;
            }
            QLineEdit#searchEdit {
                border: none;
                border-bottom: 1px solid #c0c0c0;
                border-radius: 0;
                padding: 6px 10px;
                font-size: 12px;
                background: #dedede;
            }
            QLineEdit#searchEdit:focus { background: #d4d4d4; }
            QTreeWidget#optionsTree {
                background: transparent;
                border: none;
                outline: none;
                font-size: 12px;
            }
            QTreeWidget#optionsTree::item {
                padding: 4px 4px;
                border-radius: 3px;
            }
            QTreeWidget#optionsTree::item:selected {
                background: #0078d4;
                color: white;
            }
            QTreeWidget#optionsTree::item:hover:!selected {
                background: rgba(0, 120, 212, 0.12);
            }
            QWidget#rightPanel { background: #ffffff; }
            QWidget#pageTitleBar { background: #ffffff; }
            QLabel#pageTitleLabel {
                font-size: 14px;
                font-weight: bold;
                color: #1a1a1a;
            }
            QFrame#titleSeparator { color: #e0e0e0; max-height: 1px; }
            QStackedWidget#optionsStack { background: #ffffff; }
            QFrame#buttonFrame {
                background: #f5f5f5;
                border-top: 1px solid #d0d0d0;
            }
        """)

    # ── Registry-driven population ───────────────────────────────────────────

    def _populate_from_registry(self):
        """
        Read SettingsPageRegistry and build the tree + stack.

        Group nodes are created on demand the first time a group name
        is encountered. Pages with group=None are added as top-level
        leaf items.
        """
        group_items: dict[str, QTreeWidgetItem] = {}

        for descriptor in SettingsPageRegistry.pages():
            page = descriptor.factory()
            self._pages.append(page)
            idx = self.stack.addWidget(page)

            if descriptor.group:
                if descriptor.group not in group_items:
                    group_items[descriptor.group] = self._make_group(
                        descriptor.group
                    )
                parent = group_items[descriptor.group]
            else:
                parent = None

            item = self._make_leaf(
                descriptor.title,
                descriptor.icon,
                descriptor.tooltip,
                parent,
            )

            # Use id(item) as key — QTreeWidgetItem is not hashable in PyQt
            self._page_index[id(item)] = idx

        self.tree.expandAll()

    def _make_group(self, title: str) -> QTreeWidgetItem:
        item = QTreeWidgetItem(self.tree, [title])
        item.setData(0, self._GROUP_ROLE, True)
        item.setFlags(item.flags() | Qt.ItemIsEnabled)
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        return item

    def _make_leaf(
        self,
        title: str,
        icon: QIcon,
        tooltip: str,
        parent: Optional[QTreeWidgetItem],
    ) -> QTreeWidgetItem:
        item = QTreeWidgetItem([title])
        item.setIcon(0, icon)
        item.setToolTip(0, tooltip)
        item.setData(0, self._GROUP_ROLE, False)
        if parent is not None:
            parent.addChild(item)
        else:
            self.tree.addTopLevelItem(item)
        return item

    # ── Navigation ───────────────────────────────────────────────────────────

    def _on_item_changed(self, current: QTreeWidgetItem, _prev):
        if current is None:
            return
        if current.data(0, self._GROUP_ROLE):
            current.setExpanded(True)
            if current.childCount():
                self.tree.setCurrentItem(current.child(0))
            return

        # Look up by id() — matches how we stored it in _populate_from_registry
        idx = self._page_index.get(id(current))
        if idx is not None:
            self.stack.setCurrentIndex(idx)
            self.page_title_label.setText(current.text(0))
            icon = current.icon(0)
            if not icon.isNull():
                self.page_icon_label.setPixmap(icon.pixmap(20, 20))
            else:
                self.page_icon_label.clear()

    def _select_first_leaf(self):
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            if top.data(0, self._GROUP_ROLE) and top.childCount():
                self.tree.setCurrentItem(top.child(0))
                return
            if not top.data(0, self._GROUP_ROLE):
                self.tree.setCurrentItem(top)
                return

    # ── Search ───────────────────────────────────────────────────────────────

    def _filter_tree(self, text: str):
        text = text.strip().lower()
        for i in range(self.tree.topLevelItemCount()):
            self._filter_item(self.tree.topLevelItem(i), text)

    def _filter_item(self, item: QTreeWidgetItem, text: str) -> bool:
        matches = text == "" or text in item.text(0).lower()
        child_visible = any(
            self._filter_item(item.child(i), text)
            for i in range(item.childCount())
        )
        visible = matches or child_visible
        item.setHidden(not visible)
        if text and child_visible:
            item.setExpanded(True)
        return visible

    # ── Apply / OK ───────────────────────────────────────────────────────────

    def _apply_all(self):
        for page in self._pages:
            page.apply()

    def accept(self):
        self._apply_all()
        super().accept()


# ── 3. Base application pages ─────────────────────────────────────────────────
#
#  These pages are registered once here and are present in every application
#  that imports this module.

class GeneralSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.username_edit = QLineEdit()
        layout.addRow("Username:", self.username_edit)

        self.autosave_check = QCheckBox("Enable auto-save on project close")
        layout.addRow("Auto-save:", self.autosave_check)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "German", "French", "Italian"])
        layout.addRow("Language:", self.language_combo)

        self.username_edit.setText(s.value("general/username", ""))
        self.autosave_check.setChecked(s.value("general/autosave", False, type=bool))
        self.language_combo.setCurrentText(s.value("general/language", "English"))

    def apply(self):
        s = QSettings("MyOrg", "MyApp")
        s.setValue("general/username", self.username_edit.text())
        s.setValue("general/autosave", self.autosave_check.isChecked())
        s.setValue("general/language", self.language_combo.currentText())


class DisplaySettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(6, 72)
        self.fontsize_spin.setSuffix(" pt")
        layout.addRow("Font size:", self.fontsize_spin)

        self.darkmode_check = QCheckBox("Enable dark mode")
        layout.addRow("Theme:", self.darkmode_check)

        self.fontsize_spin.setValue(s.value("display/fontsize", 10, type=int))
        self.darkmode_check.setChecked(s.value("display/darkmode", False, type=bool))

    def apply(self):
        s = QSettings("MyOrg", "MyApp")
        s.setValue("display/fontsize", self.fontsize_spin.value())
        s.setValue("display/darkmode", self.darkmode_check.isChecked())


# Register base pages — present in every application
SettingsPageRegistry.register(SettingsPageDescriptor(
    title   = "General",
    factory = GeneralSettingsPage,
    group   = "General",
    icon    = QIcon.fromTheme("preferences-other"),
    tooltip = "General application settings",
    order   = 10,
))
SettingsPageRegistry.register(SettingsPageDescriptor(
    title   = "Display",
    factory = DisplaySettingsPage,
    group   = "General",
    icon    = QIcon.fromTheme("video-display"),
    tooltip = "Font size and theme",
    order   = 20,
))


# ── 4. Custom application pages ───────────────────────────────────────────────
#
#  Register these in your own app module. They appear alongside the base pages.

class NetworkSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = QSettings("MyOrg", "AppA")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.proxy_check = QCheckBox("Use proxy server")
        layout.addRow("Proxy:", self.proxy_check)

        self.proxy_host = QLineEdit()
        self.proxy_host.setPlaceholderText("proxy.example.com")
        layout.addRow("Host:", self.proxy_host)

        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(1, 65535)
        self.proxy_port.setValue(8080)
        layout.addRow("Port:", self.proxy_port)

        self.proxy_check.setChecked(s.value("network/use_proxy", False, type=bool))
        self.proxy_host.setText(s.value("network/host", ""))
        self.proxy_port.setValue(s.value("network/port", 8080, type=int))

    def apply(self):
        s = QSettings("MyOrg", "AppA")
        s.setValue("network/use_proxy", self.proxy_check.isChecked())
        s.setValue("network/host", self.proxy_host.text())
        s.setValue("network/port", self.proxy_port.value())


class DatabaseSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = QSettings("MyOrg", "AppA")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("localhost")
        layout.addRow("Host:", self.host_edit)

        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(5432)
        layout.addRow("Port:", self.port_spin)

        self.dbname_edit = QLineEdit()
        layout.addRow("Database:", self.dbname_edit)

        self.host_edit.setText(s.value("db/host", "localhost"))
        self.port_spin.setValue(s.value("db/port", 5432, type=int))
        self.dbname_edit.setText(s.value("db/name", ""))

    def apply(self):
        s = QSettings("MyOrg", "AppA")
        s.setValue("db/host", self.host_edit.text())
        s.setValue("db/port", self.port_spin.value())
        s.setValue("db/name", self.dbname_edit.text())


# Register app-specific pages
SettingsPageRegistry.register(SettingsPageDescriptor(
    title   = "Network",
    factory = NetworkSettingsPage,
    group   = "Advanced",
    icon    = QIcon.fromTheme("network-workgroup"),
    tooltip = "Proxy and connection settings",
    order   = 10,
))
SettingsPageRegistry.register(SettingsPageDescriptor(
    title   = "Database",
    factory = DatabaseSettingsPage,
    group   = "Advanced",
    icon    = QIcon.fromTheme("server-database"),
    tooltip = "PostgreSQL connection settings",
    order   = 20,
))


# ── 5. App-specific dialog subclass ──────────────────────────────────────────
#
#  Subclass BaseSettingsDialog only when you need custom behaviour.
#  For just a different title, one line is enough.

class AppASettingsDialog(BaseSettingsDialog):
    def __init__(self, parent=None):
        super().__init__(parent, title="Application A – Settings")


# ── 6. Main window ────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom PyQGIS App")
        self.resize(420, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.status_label = QLabel("Press the button to open Settings.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        btn = QPushButton("⚙  Open Settings…")
        btn.clicked.connect(lambda: AppASettingsDialog(self).exec())
        layout.addWidget(btn)

        btn_read = QPushButton("Read & show current settings")
        btn_read.clicked.connect(self.show_settings)
        layout.addWidget(btn_read)

    def show_settings(self):
        s = QSettings("MyOrg", "MyApp")
        lines = [
            f"username : {s.value('general/username', '(not set)')}",
            f"language : {s.value('general/language', 'English')}",
            f"autosave : {s.value('general/autosave', False, type=bool)}",
            f"fontsize : {s.value('display/fontsize', 10, type=int)} pt",
            f"darkmode : {s.value('display/darkmode', False, type=bool)}",
        ]
        self.status_label.setText("\n".join(lines))


# ── 7. Bootstrap ──────────────────────────────────────────────────────────────

def main():
    from qgis.core import QgsApplication
    qgs = QgsApplication([], True)
    qgs.initQgis()

    win = MainWindow()
    win.show()

    exit_code = qgs.exec()
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()