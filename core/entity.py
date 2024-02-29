from functools import wraps
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QLabel, QMessageBox, QMainWindow

from sqlalchemy import select

from core import db_session_cm
from core.main_dialog import MainDialog


def set_data(func):
    """
    decorator-funktion um daten einzufügen oder zu bearbeiten;
    es wird außerdem die methode 'post_data_set' aufgerufen um dinge zu erledigen,
    die danach durchgeführt werden sollen

    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        content-manager-function zu einfügen und bearbeiten von datensätzen
        :param self:
        :param args:
        :param kwargs:
        :return:
        """

        func(self, *args, **kwargs)
        self.setPreMapData()
        self.mapData()

        self.post_data_set()
        self.loadSubWidgets()
        self.signals()
        self.finalInit()

    return wrapper


class Entity(QMainWindow):
    """
    baseclass um entity daten (=datensätze einer tabelle in der db) in einem
    QMainWindow zu bearbeiten;
    ein QMainWindow deshalb, weil damit auch QDochWidget eingefügt werden können
    (z.b. ein gis-kartenfenster)
    """

    _entity_mc = None  # 'mapped class' des Entities (definiert in data_model.py)
    _entity_mci = None  # Instanz der 'mapped class' des Entities
    _custom_mci = {}

    valid = True

    _entity_id = None
    _parent_id = None

    guiMainGis = None

    @property  # getter
    def entity_id(self):

        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):

        self._entity_id = value

    @property  # getter
    def parent_id(self):

        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):

        self._parent_id = value

    def __del__(self):
        print(" * * DELETE Entity * *")

        self.rejectEntity()

    def __init__(self, parent=None):
        super(Entity, self).__init__(parent)

        self.parent = parent

        self.invalid_data_text = "Die Angaben sind ungültig"

        self.entity_header_text = ''  # wird in initUI gesetzt

        self.entity_dialog = None

    def __init_subclass__(cls, *args, **kwargs):
        """
        um die methode __post_init__ direkt nach __init__ aufzurufen
        :param args:
        :param kwargs:
        :return:
        """
        super().__init_subclass__(*args, **kwargs)

        def new_init(self, *args, init=cls.__init__, **kwargs):
            init(self, *args, **kwargs)

            if cls is type(self):
                self.__post_init__()
        cls.__init__ = new_init

    def __post_init__(self):
        """
        methode die nach __init__ aufgerufen wird

        :return:
        """

        self.insertEntityHeader()
        self.initUi()
        self.setEntityTabOrder()

    def setDefaultValues(self, **kwargs):
        """
        definiere hier standardwerte die beim anlegen einer neuen entity
        gültig werden
        """
        pass

    @set_data
    def newEntity(self, new_instance=None):
        """
        lege eine neue entity an

        :param new_instance: instance der neuen entity
        """

        self._entity_mci = new_instance

        self.setDefaultValues()

    @set_data
    def editEntity(self, entity_mci=None, entity_id=None, **kwargs):
        """
        instance der entity die bearbeitet werden soll

        :param entity_mci: instanz der 'mapped class' dieses entities
        :param entity_id: id dieses entities
        :param **kwargs: z.b. mci's für die Dateneingabe (die in der gleichen
            session wie die entity_mci erstellt werden sollten
        """

        if entity_mci is not None:
            self._entity_mci = entity_mci

        if entity_id is not None:
            self.entity_id = entity_id

            with db_session_cm() as session:

                # self._entity_mci = session.get(self._entity_mc, self.entity_id)
                self._entity_mci = self.getEntityMci(session, entity_id)

                self.getCustomEntityMci(session)

        print(f'...')

    def getEntityMci(self, session, entity_id):
        """
        frage hier die mci für diese Entity ab. Bei Bedarf diese Methode
        subklassen

        :param session: session objekt
        :param entity_id: int
        :return: mci
        """

        mci = session.scalars(
            select(self._entity_mc).where(self._entity_mc.id == entity_id)
        ).unique().first()

        return mci

    def getCustomEntityMci(self, session):
        """
        frage individuelle mci's ab, die für diese Entity notwendig sind (
        z.B. mci's für die Dateneingabe)
        :param session: sqlalchemy session
        :return:
        """
        pass

    def post_data_set(self):
        """
        methode die aufgerufen wird nachdem die daten geladen wurden
        """
        pass

    def loadSubWidgets(self):
        """
        lade sub widgets
        """
        pass

    def initUi(self):
        """
        initialisiere das ui von dieser entity
        """

        """entferne die 'angreifer' im eck rechts unten die die größenänderung
                des widgets sichtbar machen"""
        self.statusBar().setSizeGripEnabled(False)
        """"""

    def focusFirst(self):
        """
        definiere hier falls notwendig das widget, das als estes den focus
        erhalten soll
        """
        pass

    def finalInit(self):
        """
        definiere hier dinge die ganz am ender der initialisierung dieser entity
        durchgeführt werden sollen
        :return:
        """
        pass

    def signals(self):
        """
        signale für diese entity
        """
        pass

    def setEntityTabOrder(self):
        """
        lege hier eine spezielle tab-order für die widgets fest (z.b. wenn
        im code zusätzlich widgets eingefügt werden
        """
        pass

    def insertEntityHeader(self):
        """
        definiere hier den kopfbereich für diese entity
        """

        if hasattr(self, 'uiHeaderWdgt'):
            self.uiHeaderWdgt.setStyleSheet("background-color: rgb(70,70,70);")

            self.guiHeaderTextLbl = QLabel(self.entity_header_text)

            self.header_label_font = QFont("Verdana", 15, QFont.Bold)
            self.header_label_style = "color: rgb(246,246,246);"

            self.guiHeaderTextLbl.setStyleSheet(self.header_label_style)
            self.guiHeaderTextLbl.setFont(self.header_label_font)
            self.uiHeaderHlay.addWidget(self.guiHeaderTextLbl)

            self.uiHeaderHlay.setContentsMargins(10, 10, 10, 10)

    def setPreMapData(self):

        pass

    def mapData(self):
        """
        mappe hier die werte der date_instance mit den entity-attributen
        """

        self.entity_id = self._entity_mci.id

    def acceptEntity(self):
        """
        definiere hier wenn das entity 'accept' wird
        """

        self.checkValidity()

        """
        überprüfe hier die gültigkeit der daten. wenn ja, dann 'commit' die daten
        und return True. andernfalls return False und setze die eigenschaft
        'valid' wieder auf True (für den nächsten validity-check)
        """
        if self.valid == True:
            self.submitEntity()
            self.commitEntity()
            return True
        elif self.valid == False:
            self.valid = True
            return False
        """"""

    def submitEntity(self):
        """
        schreibe die daten des entity in die _entity_mci
        """
        pass

    def commitEntity(self):
        """
        'commit' die daten der entity_session in die datenbank
        """
        with db_session_cm(name='commit_entity') as session:

            try:
                session.add(self._entity_mci)
            except:
                print(f'cannot add {self._entity_mci} to session')

    def rejectEntity(self):
        """
        breche ab
        """
        pass

    def checkValidity(self):
        """
        überprüfe die gültigkeit der daten dieser entity;
        wenn die daten ungültig sind dann setze 'valid' auf False
        """

    def showInvalidityMsg(self, text):
        """
        zeige eine nachricht, wenn daten ungültig sind

        noch nicht umgesetzt!!!
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Info")
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class EntityDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(EntityDialog, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

    def accept(self):
        """
        wenn 'acceptEntity' des entity-widget True zurückgibt (die daten sind
        gültig) dann rufe QDialog.accept() auf
        """
        if self.dialogWidget.acceptEntity():
            super().accept()
