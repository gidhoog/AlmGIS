from _operator import attrgetter

from qga.column import QgaTextColumn, QgaFloatColumn, QgaAreaHaColumn

from almgis.data_model import BAkt


class AktNameCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = BAkt

    def col_value(self, mci):
        return mci.name


class AktAzCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = BAkt

    def col_value(self, mci):
        return mci.az


class AktWeideareaCol(QgaAreaHaColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = BAkt

    def col_value(self, mci):

        # kop_area_ha =''
        kop_area = 0.00

        if mci.rel_abgrenzung != []:

            last_abgrenzung = max(mci.rel_abgrenzung,
                              key=attrgetter('jahr'))

            for komplex in last_abgrenzung.rel_komplex:
                for koppel in komplex.rel_koppel:
                    kop_area = kop_area + koppel.koppel_area

            # kop_area_ha = '{:.4f}'.format(
            #     round(float(kop_area) / 10000, 4)).replace(".",
            #                                                ",") + ' ha'

        # return kop_area_ha
        return kop_area

        #     if role == Qt.DisplayRole:
        #         kop_area_ha = '{:.4f}'.format(
        #             round(float(kop_area) / 10000, 4)).replace(".",
        #                                                        ",") + ' ha'
        #         return kop_area_ha
        #     if role == Qt.EditRole:
        #         return kop_area
        #
        # else:
        #     if role == Qt.DisplayRole:
        #         return '---'
        #     if role == Qt.EditRole:
        #         return 0
        # return mci.az