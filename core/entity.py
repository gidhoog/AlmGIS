from functools import wraps
from qgis.PyQt.QtWidgets import QMessageBox, QMainWindow, QDialog
from qgis.PyQt.QtCore import Qt

from sqlalchemy import select

from core import DbSession
from core.main_dialog import MainDialog
from core.tools import getMciState


# def set_data(func):
#     """
#     decorator-funktion um daten einzufügen oder zu bearbeiten;
#     es wird außerdem die methode 'postDataSet' aufgerufen um dinge zu erledigen,
#     die danach durchgeführt werden sollen
#
#     :param func:
#     :return:
#     """
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         """
#         content-manager-function zu einfügen und bearbeiten von datensätzen
#         :param self:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#
#         func(self, *args, **kwargs)
#         self.setPreMapData()
#         self.initEntityWidget()
#         self.mapEntityData()
#
#         self.postDataSet()
#         # self.loadSubWidgets()
#         self.signals()
#         self.finalEntitySettings()
#
#     return wrapper


class Entity(QMainWindow):
    """
    baseclass um entity daten (=datensätze einer tabelle in der db) in einem
    QMainWindow zu bearbeiten;
    ein QMainWindow deshalb, weil damit auch QDochWidget eingefügt werden können
    (z.b. ein gis-kartenfenster)
    """

    """'mapped class' des Entities (definiert in data_model.py); eigentlich
    nur dann notwendig, wenn die entity_mci mittels dem id von der db
    abgefragt wird"""
    # _entity_mc = None
    """"""

    _entity_mci = None  # Instanz der 'mapped class' des Entities
    # _custom_entity_data = {}

    feature = None

    valid = True

    _entity_id = None
    _parent_id = None

    _commit_on_apply = True

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
        self.edited_mci = None

        # if session:
        #     self.entity_session = session
        # else:
        self.entity_session = None

        self.purpose = 'edit'  # or 'add'

        """"""
        self._entity_mc = None
        # self._custom_entity_data = {}
        """"""
        self.entity_feature = None

        self.invalid_data_text = "Die Angaben sind ungültig"

        self.entity_header_text = ''  # wird in initUI gesetzt

        self.entity_dialog = None

    def setEntitySession(self, session):

        self.entity_session = session

    def setDefaultValues(self, **kwargs):
        """
        definiere hier standardwerte die beim anlegen einer neuen entity
        gültig werden
        """
        pass

    # @set_data
    def newEntity(self, new_instance=None):
        """
        lege eine neue entity an

        :param new_instance: instance der neuen entity
        """

        self._entity_mci = new_instance

        self.setDefaultValues()


    def assembleEntityWidget(self):
        """
        put the entity-widget together
        """
        self.prepareEntity()

        self.loadBackgroundData()

        self.mapEntityData()

        self.setupDataUi()

        self.postDataSet()

        self.focusFirst()

        self.setElementTabOrder()

        self.finalEntitySettings()

        self.signals()

    def prepareEntity(self):
        """
        z.B. übergebe die session an diverse widgets
        :return:
        """

    def loadBackgroundData(self):
        """
        define and configure data for elements in this entity-widget
        (e.g. combo-data, ...)
        """
        pass

    def setupDataUi(self):
        """
        define here data-based ui-settings
        """
        if hasattr(self._entity_mci, 'rel_type'):
            self.setTypeProperties()

    def setupCodeUi(self):
        """
        define code-based ui-settings

        :return:
        """
        # self.insertEntityHeader()

    def setElementTabOrder(self):
        """
        definiere die Tab-order von widgets die im code eingefügt wurden
        :return:
        """

    # @set_data
    def editEntity(self, entity_mci=None, entity_id=None, feature=None,
                   edited_mci=None, **kwargs):
        """
        instance der entity die bearbeitet werden soll

        :param entity_mci: instanz der 'mapped class' dieses entities
        :param entity_id: id dieses entities
        :param **kwargs: z.b. mci's für die Dateneingabe (die in der gleichen
            session wie die entity_mci erstellt werden sollten
        """
        self.edited_mci = edited_mci
        self.entity_feature = feature

        if entity_id is not None:
            self.entity_id = entity_id
            self._entity_mci = self.entity_session.get(self._entity_mc,
                                                       self.entity_id)

        else:
            self._entity_mci = entity_mci

        self.assembleEntityWidget()

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

    def postDataSet(self):
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

    def finalEntitySettings(self):
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

    def setTypeProperties(self):
        """set type-specific values, layout, appearance, ..."""

        pass

    def initEntityWidget(self):

        # self.insertEntityHeader()
        self.initUi()
        self.setEntityTabOrder()

    def setPreMapData(self):

        pass

    def mapEntityData(self):
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
        überprüfe hier die gültigkeit der daten. wenn ja, dann 'submit' die daten;
        ggf. 'commite' die daten (wenn commit_on_apply' True ist) und return True;
        andernfalls return False und setze die eigenschaft
        'valid' wieder auf True (für den nächsten validity-check)
        """
        if self.valid == True:
            self.submitEntity()
            if self._commit_on_apply:
                self.commitEntity()

            return self._entity_mci
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

        self.entity_session.commit()
        self.entity_session.close()

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

        self.accepted_mci = None
        self.edited_mci = None

        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def accept(self):
        super().accept()

        self.accepted_mci = self.dialogWidget.acceptEntity()
        self.edited_mci = self.dialogWidget.edited_mci

        # QDialog.accept(self)
