# https://www.perplexity.ai/search/create-two-tables-based-on-a-q-6DdXgTLrTt2Ghf6E5Aii0g

import sys

from qgis._core import QgsFeature, QgsVectorLayerCache
from qgis._gui import QgsAttributeTableView, QgsAttributeTableModel, \
    QgsMapCanvas
from qgis.core import QgsApplication, QgsVectorLayer, QgsRelation, edit
from qgis.gui import QgsAttributeTableFilterModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter

class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create parent and child layers
        self.parent_layer = QgsVectorLayer("None?field=id:integer&field=name:string", "Parent", "memory")
        self.child_layer = QgsVectorLayer("None?field=id:integer&field=parent_id:integer&field=child_data:string", "Child", "memory")

        # Add sample data
        with edit(self.parent_layer):
            p1 = QgsFeature(self.parent_layer.fields())
            p1.setAttributes([1, "Parent 1"])
            self.parent_layer.addFeature(p1)
            p2 = QgsFeature(self.parent_layer.fields())
            p2.setAttributes([2, "Parent 2"])
            self.parent_layer.addFeature(p2)

        with edit(self.child_layer):
            c1 = QgsFeature(self.child_layer.fields())
            c1.setAttributes([1, 1, "Child 1-1"])
            self.child_layer.addFeature(c1)
            c2 = QgsFeature(self.child_layer.fields())
            c2.setAttributes([2, 1, "Child 1-2"])
            self.child_layer.addFeature(c2)
            c3 = QgsFeature(self.child_layer.fields())
            c3.setAttributes([3, 2, "Child 2-1"])
            self.child_layer.addFeature(c3)

        # Create relation
        relation = QgsRelation()
        relation.setId("parent_child")
        relation.setName("Parent-Child")
        relation.setReferencingLayer(self.child_layer.id())
        relation.setReferencedLayer(self.parent_layer.id())
        relation.addFieldPair("parent_id", "id")
        relation.isValid()  # Should return True

        # Create main window
        # widget = QWidget()
        layout = QVBoxLayout()
        splitter = QSplitter()

        # Create attribute table views
        self.parent_view = QgsAttributeTableView()
        self.child_view = QgsAttributeTableView()

        # Set models with relation filtering
        self.parent_cache = QgsVectorLayerCache(self.parent_layer, 100000)
        self.parent_model = QgsAttributeTableModel(self.parent_cache)
        self.parent_model.loadLayer()
        self.parent_filter_model = QgsAttributeTableFilterModel(QgsMapCanvas(), self.parent_model)
        # parent_filter_model.setSourceModel(parent_model)
        self.parent_view.setModel(self.parent_filter_model)

        self.child_cache = QgsVectorLayerCache(self.child_layer, 100000)
        self.child_model = QgsAttributeTableModel(self.child_cache)
        self.child_model.loadLayer()
        self.child_filter_model = QgsAttributeTableFilterModel(QgsMapCanvas(), self.child_model)
        # child_filter_model.setSourceModel(child_model)
        self.child_view.setModel(self.child_filter_model)

        self.parent_view.selectionModel().selectionChanged.connect(self.filter_child_table)

        # Layout setup
        splitter.addWidget(self.parent_view)
        splitter.addWidget(self.child_view)
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Connect selection events
    def filter_child_table(self):
        selected = self.parent_view.selectionModel().selectedRows()
        if selected:
            parent_id = self.parent_layer.getFeature(selected[0].row())["id"]
            self.child_filter_model.setFilterExpression(f'"parent_id" = {parent_id}')
        else:
            self.child_filter_model.setFilterExpression("")

# widget.show()
#
# # Execute application
# # qgs.exec_()
# # qgs.exitQgis()
# sys.exit(qgs.exec_())

if __name__ == "__main__":
    # Initialize QGIS application
    # from qgis.core import QgsApplication

    qgs = QgsApplication([], True)
    qgs.setPrefixPath("/var/lib/flatpak/app/org.qgis.qgis",
                          True)
    qgs.initQgis()

    # Create and show the main window
    # app = QApplication(sys.argv)
    wdg = Widget()
    wdg.show()

    # # Run the application
    # exit_code = app.exec_()
    #
    # # Exit QGIS
    # qgs.exitQgis()
    #
    # sys.exit(exit_code)
    sys.exit(qgs.exec_())
