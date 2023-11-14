import math
from datetime import datetime

from qgis.PyQt.QtCore import Qt, QRectF, QPointF
from qgis.PyQt.QtGui import QFont, QPolygonF
from qgis.core import QgsPrintLayout, QgsUnitTypes, QgsLayoutItemPage,\
    QgsLayoutItemLabel, QgsProject, QgsLayoutItemPicture, QgsLayoutItemPolygon, \
    QgsLayoutTableColumn, QgsLayoutItemTextTable, QgsLayoutFrame, \
    QgsLayoutPoint, QgsLayoutSize, QgsLayoutItemMap, QgsRectangle, \
    QgsLayoutItemHtml
from sqlalchemy import func, and_, desc
from core import db_session_cm
from core.data_model import BGst, BKatGem, BGstEz, BGstZuordnung, BGstVersion, \
    BGisScopeLayer
from core.gis_layer import getGisLayer, setLayerStyle

from core.tools import convertMtoHa


class AwbAuszug(QgsPrintLayout):

    # todo: füge einen layer mit den gst von nögis ein!!!

    def __init__(self, akt_instance=None):
        """
        baseclass für die erstellung eines alm- und weidebuch auszuges
        """

        """erstelle eine QgsProjekt-Instanz, die u.a. als parent
        für ein QgsPrintLayout notwendig ist"""
        self.qgs_project_instance = QgsProject()
        """"""
        super(AwbAuszug, self).__init__(self.qgs_project_instance)

        self.akt_instance = akt_instance

        self.initializeDefaults()
        self.setUnits(QgsUnitTypes.LayoutMillimeters)

        """erzeuge eine Variable für die seitensammlung"""
        self.page_collection = self.pageCollection()

        """definiere die erste seite"""
        self.page_collection.page(0).setPageSize(
            'A4', QgsLayoutItemPage.Orientation.Portrait)

        """setze die Seitenränder"""
        self.left_margin = 20
        self.right_margin = 15
        self.top_margin = 15
        self.bottom_margin = 15

        self.page_with = 210
        self.page_height = 297
        """"""

        """hole die daten"""
        with db_session_cm() as session:
            session.expire_on_commit = False

            self.gst_query = session.query(BGst.kgnr,
                                      BKatGem.kgname,
                                      BGstEz.ez,
                                      BGst.gst,
                                      func.ST_Area(BGstVersion.geometry),
                                      func.max(BGstEz.datenstand)) \
                .select_from(BGstZuordnung) \
                .join(BGst) \
                .join(BGstVersion) \
                .join(BGstEz) \
                .join(BKatGem) \
                .filter(and_(BGstZuordnung.akt_id == self.akt_instance.id,
                             BGstZuordnung.awb_status_id == 1)) \
                .group_by(BGstZuordnung.id) \
                .all()

        self.hoch = self.top_margin

        self.insertDeckblatt()

        new_page = QgsLayoutItemPage(self)
        self.page_collection.addPage(new_page)

        """definiere die seite mit der karte"""
        self.page_collection.page(1).setPageSize(
            'A3', QgsLayoutItemPage.Orientation.Landscape)

        self.insertMapPage()

    def insertDeckblatt(self):
        """
        füge die erste Seite (die Gst-Tabelle) ein
        """
        self.insertHeader()
        self.insertTitel()
        self.insertAwbDetails()
        self.insertSeitennummer()
        self.insertGstTable()

    def insertHeader(self):
        """
        füge einen Kopf mit Logo, Adresse und Datenstand ein
        """
        abb_name = 'NÖ Agrarbezirksbehörde'
        abb_name_font = QFont('Arial', 14)
        abb_name_font.setBold(True)
        abb_name_label = QgsLayoutItemLabel(self)
        abb_name_label.setText(abb_name)
        abb_name_label.setPos(self.left_margin + 63, self.hoch)
        abb_name_label.setFont(abb_name_font)
        abb_name_label.adjustSizeToText()
        self.addLayoutItem(abb_name_label)

        abb_adresse = '3109 St. Pölten, Landhausplatz 1/12'
        abb_adresse_font = QFont('Arial', 10)
        abb_adresse_label = QgsLayoutItemLabel(self)
        abb_adresse_label.setText(abb_adresse)
        abb_adresse_label.setPos(self.left_margin + 63, self.hoch + 5.5)
        abb_adresse_label.setFont(abb_adresse_font)
        abb_adresse_label.adjustSizeToText()
        self.addLayoutItem(abb_adresse_label)

        """füge das ABB-Logo ein"""
        logo = QgsLayoutItemPicture(self)
        logo.setPicturePath(':/logo/resources/icons/abb_logo_ohne_schrift.svg')
        logo.attemptSetSceneRect(QRectF(self.left_margin + 47, self.hoch, 14, 10))
        self.addLayoutItem(logo)
        """"""

        """füge eine Linie unterhalb der Adresse ein"""
        line = QPolygonF()
        line.append(QPointF(self.left_margin, self.hoch + 11.0))
        line.append(QPointF(self.page_with - self.right_margin, self.hoch + 11.0))
        adress_line = QgsLayoutItemPolygon(line, self)
        self.addLayoutItem(adress_line)
        """"""

        """füge das Datum für den Datenstand ein"""
        today = datetime.now().strftime('%d. %B %Y')
        datenstand_string = 'erstellt am:  ' + today
        datenstand_font = QFont('Arial', 9)

        datenstand = QgsLayoutItemLabel(self)

        datenstand.setText(datenstand_string)
        datenstand.setFont(datenstand_font)
        datenstand.adjustSizeToText()
        datenstand_width = datenstand.sizeForText().width()
        datenstand.setPos(self.page_with - self.right_margin - datenstand_width - 5, self.hoch + 12)
        self.addLayoutItem(datenstand)
        """"""

        self.hoch += 32

    def insertTitel(self):
        """
        füge den Seitentitel ein
        """

        titel_string = 'NÖ Alm- und Weidebuch'
        titel = QgsLayoutItemLabel(self)
        titel_font = QFont('Arial', 20)
        titel_font.setBold(True)
        titel.setText(titel_string)
        titel.setFont(titel_font)
        titel.adjustSizeToText()
        titel_width = titel.sizeForText().width()
        titel.setPos((self.page_with / 2) - (titel_width / 2), self.hoch)
        self.addLayoutItem(titel)

        self.hoch += 20

    def insertAwbDetails(self):
        """
        füge die Detailinfos für den AWB-Auszug ein
        """
        label_font = QFont('Arial', 10)
        value_font = QFont('Arial', 12)
        value_font.setBold(True)

        az_string = 'Aktenzahl:'
        az = QgsLayoutItemLabel(self)
        az.setText(az_string)
        az.setFont(label_font)
        az.adjustSizeToText()
        az.setPos(self.left_margin, self.hoch)
        self.addLayoutItem(az)

        az_label_width = az.sizeForText().width()

        az_value_string = str(self.akt_instance.az)
        az_value = QgsLayoutItemLabel(self)
        az_value.setText(az_value_string)
        az_value.setFont(value_font)
        az_value.adjustSizeToText()
        az_value.setPos(self.left_margin + az_label_width + 5, self.hoch - 0.5)
        self.addLayoutItem(az_value)

        name_string = 'Name:'
        name = QgsLayoutItemLabel(self)
        name.setText(name_string)
        name.setFont(label_font)
        name.adjustSizeToText()
        name_label_width = name.sizeForText().width()

        name.setPos(self.left_margin + az_label_width - name_label_width, self.hoch + 10)
        self.addLayoutItem(name)

        name_value_string = str(self.akt_instance.name)
        name_value = QgsLayoutItemLabel(self)
        name_value.setText(name_value_string)
        name_value.setFont(value_font)
        name_value.adjustSizeToText()
        name_value.setPos(self.left_margin + az_label_width + 5, self.hoch + 9.5)
        self.addLayoutItem(name_value)

    def insertSeitennummer(self):
        """füge die Seitennummer ein"""

        seitennummer = QgsLayoutItemLabel(self)
        seitennummer_font = QFont('Arial', 8)
        seitennummer_string = 'Seite 1 von 2'
        seitennummer.setText(seitennummer_string)
        seitennummer.setFont(seitennummer_font)
        seitennummer.adjustSizeToText()
        seitennummer.setPos(self.page_with - self.right_margin - 17,
                            self.page_height - self.bottom_margin + 2)
        self.addItem(seitennummer)
        """"""
    def insertGstTable(self):
        """füge die Grundstückstabelle, wenn vorhanden, ein"""

        label_font = QFont('Arial', 10)

        if self.gst_query:

            self.hoch += 20

            gst_label = QgsLayoutItemLabel(self)
            gst_label_string = 'eingetragene Grundstücke:'
            gst_label.setText(gst_label_string)
            gst_label.setFont(label_font)
            gst_label.adjustSizeToText()
            gst_label.setPos(self.left_margin, self.hoch)
            self.addItem(gst_label)

            self.hoch += 5

            gst_table = QgsLayoutItemTextTable(self)

            gst_table_width = self.page_with - self.left_margin - self.right_margin

            kgnr = QgsLayoutTableColumn()
            kgnr.setHeading('Kg-Nr')
            kgnr.setWidth(gst_table_width * 0.09)
            kgnr.setHAlignment(Qt.AlignHCenter)

            kgname = QgsLayoutTableColumn()
            kgname.setHeading('Kg-Name')
            kgname.setWidth(gst_table_width * 0.22)

            ez = QgsLayoutTableColumn()
            ez.setHeading('EZ')
            ez.setWidth(gst_table_width * 0.09)
            ez.setHAlignment(Qt.AlignHCenter)

            gst = QgsLayoutTableColumn()
            gst.setHeading('Gst')
            gst.setWidth(gst_table_width * 0.09)
            gst.setHAlignment(Qt.AlignHCenter)

            area = QgsLayoutTableColumn()
            area.setHeading('Fläche (ha)')
            area.setWidth(gst_table_width * 0.18)
            area.setHAlignment(Qt.AlignRight)

            datenstand = QgsLayoutTableColumn()
            datenstand.setHeading('Datenstand')
            datenstand.setWidth(gst_table_width * 0.22)
            datenstand.setHAlignment(Qt.AlignRight)

            gst_table.setColumns([kgnr, kgname, ez, gst, area, datenstand])

            gst_stringlist = []

            gst_table_height = 7.1 + (float(len(self.gst_query)) * 7.1)

            area_sum = 0

            for gst in self.gst_query:
                gst_row = []
                col_id = 0
                for col in gst:
                    if col_id == 4:  # fläche
                        area_sum = area_sum + int(col)
                        gst_row.append(str(convertMtoHa(float(col))))
                    elif col_id == 5:  # datenstand
                        # erzeuge datetime-objekt aus string
                        stand = datetime.strptime(str(col), '%Y-%m-%d %H:%M:%S')
                        # erzeuge fromatierten string aus dem datetime-objekt
                        gst_row.append(
                            stand.strftime('%d. %B %Y'))
                    else:
                        gst_row.append(str(col))
                    col_id += 1
                gst_stringlist.append(gst_row)

            gst_table.setContents(gst_stringlist)

            self.addMultiFrame(gst_table)

            gst_frame = QgsLayoutFrame(self, gst_table)
            gst_frame.attemptMove(QgsLayoutPoint(
                self.left_margin, self.hoch, QgsUnitTypes.LayoutMillimeters))
            gst_table.recalculateTableSize()
            gst_frame.attemptResize(QgsLayoutSize(
                gst_table_width, gst_table_height), True)
            gst_table.addFrame(gst_frame)

            self.hoch += gst_table_height + 5

            """füge die Grundstücksanzahl ein"""
            if len(self.gst_query) != 0:
                table_footer_font = QFont('Arial', 10)

                gst_count_label = QgsLayoutItemLabel(self)

                if len(self.gst_query) == 1:
                    gst_count_string = '1 Grundstück eingetragen'
                else:
                    gst_count_string = str(len(self.gst_query)) + \
                                       ' Grundstücke eingetragen'

                gst_count_label.setText(gst_count_string)
                gst_count_label.setFont(table_footer_font)
                gst_count_label.adjustSizeToText()
                gst_count_label.setPos(self.left_margin, self.hoch)
                self.addItem(gst_count_label)
                """"""

                """füge die Flächensumme ein"""
                area_sum_label = QgsLayoutItemLabel(self)
                area_sum_label_string = 'eingetragene Gesamtfläche:    ' + \
                                        str(convertMtoHa(float(area_sum))) + ' ha'
                area_sum_label.setText(area_sum_label_string)
                area_sum_label.setFont(table_footer_font)
                area_sum_label.adjustSizeToText()
                area_sum_label.setPos(self.left_margin, self.hoch + 9.5)
                self.addItem(area_sum_label)
                """"""

        else:
            self.hoch += 20

            no_gst_label = QgsLayoutItemLabel(self)
            no_gst_label_string = 'Zu diesem Akt sind keine Grundstücke ' \
                                  'im NÖ Alm- und Weidebuch eingetragen.'
            no_gst_label.setText(no_gst_label_string)
            no_gst_label.setFont(label_font)
            no_gst_label.adjustSizeToText()
            no_gst_label.setPos(self.left_margin, self.hoch)
            self.addItem(no_gst_label)

    def insertMapPage(self):

        self.page = 1

        """setze die Seitenränder"""
        self.left_margin = 20
        self.right_margin = 15
        self.top_margin = 20
        self.bottom_margin = 15

        self.page_with = 420
        self.page_height = 297
        """"""

        self.info_block_height = 20

        self.hoch = self.top_margin
        self.rechts = self.left_margin

        self.insertMapHeader()
        self.insertMap()

    def insertMapHeader(self):

        """Rahmen für header"""
        xmin = self.left_margin
        ymin = self.hoch
        xmax = self.page_with - self.right_margin
        ymax = ymin + self.info_block_height
        scale_frame = QPolygonF()
        scale_frame.append(QPointF(xmin, ymin))
        scale_frame.append(QPointF(xmax, ymin))
        scale_frame.append(QPointF(xmax, ymax))
        scale_frame.append(QPointF(xmin, ymax))

        # Create the polygon from nodes
        polygonItem = QgsLayoutItemPolygon(scale_frame, self)
        polygonItem.attemptMove(QgsLayoutPoint(
            self.rechts, self.hoch, QgsUnitTypes.LayoutMillimeters),
            page=self.page)

        # Add to the layout
        self.addLayoutItem(polygonItem)

        """füge das ABB-Logo ein"""
        logo = QgsLayoutItemPicture(self)
        logo.setPicturePath(':/logo/resources/icons/abb_logo_ohne_schrift.svg')
        logo.attemptSetSceneRect(QRectF(self.rechts + 5, self.hoch + 4.5, 15, 10))
        logo.attemptMove(QgsLayoutPoint(self.rechts + 5, self.hoch + 4.5, QgsUnitTypes.LayoutMillimeters),
                            page=self.page)
        self.addLayoutItem(logo)
        """"""

        abb_name = 'NÖ Agrarbezirksbehörde'
        abb_name_font = QFont('Arial', 14)
        abb_name_font.setBold(True)
        abb_name_label = QgsLayoutItemLabel(self)
        abb_name_label.setText(abb_name)
        abb_name_label.attemptMove(
            QgsLayoutPoint(self.rechts + 22, self.hoch + 4.5,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        abb_name_label.setFont(abb_name_font)
        abb_name_label.adjustSizeToText()
        self.addLayoutItem(abb_name_label)

        abb_adresse = '3109 St. Pölten, Landhausplatz 1/12'
        abb_adresse_font = QFont('Arial', 10)
        abb_adresse_label = QgsLayoutItemLabel(self)
        abb_adresse_label.setText(abb_adresse)
        abb_adresse_label.attemptMove(
            QgsLayoutPoint(self.rechts + 22, self.hoch + 10.5,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        abb_adresse_label.setFont(abb_adresse_font)
        abb_adresse_label.adjustSizeToText()
        self.addLayoutItem(abb_adresse_label)

        self.rechts += 96

        """füge eine Linie rechts der Adresse ein"""
        line = QPolygonF()
        line.append(QPointF(self.rechts, self.hoch))
        line.append(QPointF(self.rechts, self.hoch + self.info_block_height))
        adress_line = QgsLayoutItemPolygon(line, self)
        adress_line.attemptMove(
            QgsLayoutPoint(self.rechts, self.hoch,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(adress_line)
        """"""

        self.rechts += 10

        """füge den Kartentitel ein"""
        titel = QgsLayoutItemLabel(self)
        titel_string = 'Karte zum NÖ Alm- und Weidebuch'
        titel_font = QFont('Arial', 16)
        titel_font.setBold(True)
        titel.setText(titel_string)
        titel.setFont(titel_font)
        titel.adjustSizeToText()
        titel.attemptMove(
            QgsLayoutPoint(self.rechts, self.hoch + 7.5,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(titel)

        self.rechts += 105

        """füge eine Linie rechts des Titels ein"""
        t_line = QPolygonF()
        t_line.append(QPointF(self.rechts, self.hoch))
        t_line.append(QPointF(self.rechts, self.hoch + self.info_block_height))
        titel_line = QgsLayoutItemPolygon(t_line, self)
        titel_line.attemptMove(
            QgsLayoutPoint(self.rechts, self.hoch,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(titel_line)
        """"""

        """füge die Beschreibung zur Karte ein"""
        map_html = QgsLayoutItemHtml(self)
        map_html_frame = QgsLayoutFrame(self, map_html)
        map_html_frame.attemptSetSceneRect(QRectF(10, 10, 60, 15))
        map_html.addFrame(map_html_frame)

        map_html.setContentMode(QgsLayoutItemHtml.ManualHtml)
        map_html.setHtml(
            '''<body style="margin:0;"><p style="font-family:arial; 
            font-size:12px">
            Darstellung der im NÖ Alm- und Weidebuch eingetragenen 
            Grundstücke (blau).</p></body>''')
        map_html.loadHtml()
        map_html_frame.attemptMove(
            QgsLayoutPoint(self.rechts + 3, self.hoch + 5,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(map_html_frame)
        """"""
        self.rechts += 68

        """füge eine Linie rechts der Bechreibung ein"""
        d_line = QPolygonF()
        d_line.append(QPointF(self.rechts, self.hoch))
        d_line.append(QPointF(self.rechts, self.hoch + self.info_block_height))
        descr_line = QgsLayoutItemPolygon(d_line, self)
        descr_line.attemptMove(
            QgsLayoutPoint(self.rechts, self.hoch,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(descr_line)
        """"""

        detail_label_font = QFont('Arial', 8)
        detail_value_font = QFont('Arial', 8)
        detail_value_font.setBold(True)

        az = QgsLayoutItemLabel(self)
        az_string = 'Aktenzahl:'
        az.setText(az_string)
        az.setFont(detail_label_font)
        az.adjustSizeToText()
        az.attemptMove(QgsLayoutPoint(self.rechts + 2, self.hoch + 4,
                                      QgsUnitTypes.LayoutMillimeters),
                                page=self.page)
        self.addItem(az)

        """füge die aktenzahl ein"""
        az_value = QgsLayoutItemLabel(self)
        az_value_string = str(self.akt_instance.az)
        az_value.setText(az_value_string)
        az_value.setFont(detail_value_font)
        az_value.adjustSizeToText()
        az_value.attemptMove(
            QgsLayoutPoint(self.rechts + 23, self.hoch + 4.8,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(az_value)
        """"""

        name = QgsLayoutItemLabel(self)
        name_string = 'Name:'
        name.setText(name_string)
        name.setFont(detail_label_font)
        name.adjustSizeToText()
        name.attemptMove(QgsLayoutPoint(
            self.rechts + 2, self.hoch + 9,
            QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(name)

        """füge den namen ein"""
        name_value = QgsLayoutItemLabel(self)
        name_value_string = str(self.akt_instance.name)
        name_value.setText(name_value_string)
        name_value.setFont(detail_value_font)
        name_value.adjustSizeToText()
        name_value.attemptMove(
            QgsLayoutPoint(self.rechts + 23, self.hoch + 9.8,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(name_value)
        """"""

        datenstand = QgsLayoutItemLabel(self)
        datenstand_string = 'Datenstand:'
        datenstand.setText(datenstand_string)
        datenstand.setFont(detail_label_font)
        datenstand.adjustSizeToText()
        datenstand.attemptMove(QgsLayoutPoint(self.rechts + 2, self.hoch + 14, QgsUnitTypes.LayoutMillimeters),
                                page=self.page)
        self.addLayoutItem(datenstand)

        datenstand_value = QgsLayoutItemLabel(self)
        today = datetime.now().strftime('%d. %B %Y')
        datenstand_value_string = today
        datenstand_value.setText(datenstand_value_string)
        datenstand_value.setFont(detail_value_font)
        datenstand_value.adjustSizeToText()
        datenstand_value.attemptMove(QgsLayoutPoint(self.rechts + 23, self.hoch + 14.8,
                                                    QgsUnitTypes.LayoutMillimeters),
                                page=self.page)
        self.addLayoutItem(datenstand_value)

        self.rechts += 65

        """füge eine Linie rechts der Aktendetails ein"""
        a_line = QPolygonF()
        a_line.append(QPointF(self.rechts, self.hoch))
        a_line.append(QPointF(self.rechts, self.hoch + self.info_block_height))
        akt_line = QgsLayoutItemPolygon(a_line, self)
        akt_line.attemptMove(QgsLayoutPoint(self.rechts, self.hoch, QgsUnitTypes.LayoutMillimeters),
                               page=self.page)
        self.addLayoutItem(akt_line)
        """"""

        """füge Maßstabs-Infos ein"""
        scale_string = 'Maßstab'
        scale = QgsLayoutItemLabel(self)
        scale.setText(scale_string)
        scale_font = QFont('Arial', 12)
        scale.setFont(scale_font)
        scale.adjustSizeToText()
        scale.attemptMove(
            QgsLayoutPoint(self.rechts + 4, self.hoch + 5,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addLayoutItem(scale)

        """der maßstabswert wird nach dem einfügen der karte eingefügt!"""

        """füge einen Nordpfeil ein"""
        north = QgsLayoutItemPicture(self)
        north.setPicturePath(':/logo/resources/icons/nordpfeil01.png')
        north.attemptSetSceneRect(QRectF(self.rechts + 30, self.hoch + 4, 10, 15))
        north.attemptMove(
            QgsLayoutPoint(self.rechts + 28, self.hoch + 4,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addItem(north)
        """"""

        """füge die Seitennummer ein"""
        seitennummer = QgsLayoutItemLabel(self)
        seitennummer_font = QFont('Arial', 8)
        seitennummer_string = 'Seite 2 von 2'
        seitennummer.setText(seitennummer_string)
        seitennummer.setFont(seitennummer_font)
        seitennummer.adjustSizeToText()
        seitennummer.attemptMove(
            QgsLayoutPoint(self.page_with - self.right_margin - 17,
                           self.page_height - self.bottom_margin + 2,
                           QgsUnitTypes.LayoutMillimeters), page=self.page)
        self.addItem(seitennummer)
        """"""

    def insertMap(self):

        if self.gst_query:

            map_height = self.page_height - self.top_margin - self.bottom_margin - self.info_block_height
            map_width = self.page_with - self.left_margin - self.right_margin
            self.layout_map = QgsLayoutItemMap(self)

            self.layout_map.attemptMove(
                QgsLayoutPoint(self.left_margin,
                               self.hoch + self.info_block_height,
                               QgsUnitTypes.LayoutMillimeters), page=self.page)
            self.layout_map.attemptResize(
                QgsLayoutSize(map_width, map_height,
                              QgsUnitTypes.LayoutMillimeters))

            self.layout_map.setFrameEnabled(True)

            map_layers = []
            extent = QgsRectangle()
            extent.setMinimal()

            """hole die layer für die karte"""
            with db_session_cm() as session:

                map_layer_query = session.query(BGisScopeLayer)\
                    .filter(BGisScopeLayer.gis_scope_id == 3) \
                    .order_by(desc(BGisScopeLayer.order)) \
                    .all()

                for scope_layer_instance in map_layer_query:

                    layer_style_inst = scope_layer_instance.rel_gis_style

                    if scope_layer_instance.base_id_column or scope_layer_instance.feat_filt_expr:
                        id_column = scope_layer_instance.base_id_column

                        gis_layer = getGisLayer(layer_instance=layer_style_inst,
                                                base_id_column=id_column,
                                                id_val=self.akt_instance.id,
                                                feat_filt_expr=scope_layer_instance.feat_filt_expr)
                    else:
                        gis_layer = getGisLayer(layer_instance=layer_style_inst)

                    if layer_style_inst.qml_file:
                        setLayerStyle(gis_layer, layer_style_inst.qml_file)

                    if scope_layer_instance.baselayer:
                        extent.combineExtentWith(gis_layer.extent())

                    map_layers.append(gis_layer)
            """"""

            self.layout_map.setLayers(map_layers)
            self.qgs_project_instance.addMapLayers(map_layers)
            self.layout_map.setExtent(extent)
            self.layout_map.attemptResize(
                QgsLayoutSize(map_width, map_height,
                              QgsUnitTypes.LayoutMillimeters))
            self.layout_map.zoomToExtent(extent)

            """setzte das crs für das layout um den maßstab richtig zu bekommen"""
            map_crs = self.layout_map.crs()
            map_crs.createFromId(31259)
            self.layout_map.setCrs(map_crs)
            """"""

            scale = self.layout_map.scale()  # hole den maßstab

            """vergrößere den maßstab etwas und rund zum nächsten 100er;
            für eine bessere platzierung der darzustellenden gst"""
            scale_display = scale * 1.03
            scale_new = int(math.ceil(scale_display / 100.0)) * 100  # runde
            self.layout_map.setScale(scale_new, True)
            """"""

            self.addItem(self.layout_map)

            """füge den maßstab ein hinzu"""
            scale_string = f'1 : {str(scale_new)}'
            scale_font = QFont('Arial', 11)
            scale_font.setBold(True)

            scale_label = QgsLayoutItemLabel(self)
            scale_label.setText(scale_string)
            scale_label.setFont(scale_font)
            scale_label.adjustSizeToText()
            scale_label.attemptMove(
                QgsLayoutPoint(370, 32,
                               QgsUnitTypes.LayoutMillimeters), page=self.page)
            self.addLayoutItem(scale_label)
            """"""
