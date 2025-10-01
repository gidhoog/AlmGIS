import os
from datetime import datetime
from typing import List

from uuid import uuid4, UUID

from qga.database.alchemy import DmBaseProject, DmNonSpatialObject, DmBaseCommon
# from qga.alchemy import DmBaseProject, DmNonSpatialObject, DmBaseCommon
from qgis.core import QgsGeometry

from geoalchemy2 import Geometry, WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

# class DmBaseProject(DeclarativeBase):
#     pass


class DmAkt(DmNonSpatialObject, DmBaseProject):
    """
    basisdatenebene für akte
    """
    __tablename__ = "_tbl_alm_akt"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    alias: Mapped[str]
    az: Mapped[int]
    bewirtschafter_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_kontakt.id"))
    bearbeitungsstatus_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_bearbeitungsstatus.id"))
    # bearbeitungsstatus_id = Column(Integer, ForeignKey('a_alm_bearbeitungsstatus.id'))
    alm_bnr: Mapped[int]
    anm: Mapped[str]
    stz: Mapped[str]
    wwp: Mapped[bool]
    wwp_exist: Mapped[bool]
    wwp_date: Mapped[str]
    weidedauer: Mapped[int]
    max_gve: Mapped[float]
    nicht_bewirtschaftet: Mapped[bool]

    # rel_bearbeitungsstatus = relationship('DmBearbeitungsstatus')
    rel_bearbeitungsstatus: Mapped["DmBearbeitungsstatus"] = relationship(lazy='joined')
    rel_bewirtschafter: Mapped["DmKontakt"] = relationship(lazy='joined',
                                                           back_populates='rel_akt')

    # rel_gst_zuordnung = relationship(
    #     'DmGstZuordnung',
    #     back_populates='rel_akt')
    rel_gst_zuordnung: Mapped[List["DmGstZuordnung"]] = relationship(
        back_populates='rel_akt')

    # rel_komplex_name = relationship('DmKomplexName', back_populates='rel_akt')
    rel_komplex_name: Mapped[List["DmKomplexName"]] = relationship(
        back_populates='rel_akt')

    # rel_abgrenzung = relationship('DmAbgrenzung',
    #                               back_populates='rel_akt',
    #                               cascade="all, delete, delete-orphan")
    rel_abgrenzung: Mapped[List["DmAbgrenzung"]] = relationship(
        back_populates='rel_akt',
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<DmAkt(id='%s', name='%s', az='%s')>" % (
                            self.id, self.name, self.az)


class DmBanu(DmBaseProject):
    """
    Datenebene für den banu-Wert
    """
    __tablename__ = '_tbl_alm_banu'

    id: Mapped[int] = mapped_column(primary_key=True)
    ba_id: Mapped[int]
    ba_name: Mapped[str]
    ba_name_short: Mapped[str]
    nu_id: Mapped[int]
    nu_name: Mapped[str]
    nu_name_short: Mapped[str]
    symbol: Mapped[int]

    rel_alm_gst_nutzung: Mapped["DmGstNutzung"] = relationship(
        back_populates='rel_banu')


class DmBearbeitungsstatus(DmBaseProject):
    """
    basisdatenebene für den bearbeitungsstatus
    """
    __tablename__ = '_tbl_alm_bearbeitungsstatus'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_short = Column(String)
    sort = Column(Integer)
    color = Column(String)

    def __repr__(self):
        return f"<DmBearbeitungsstatus(id={self.id}, name='{self.name}')>"


class DmCutKoppelGstAktuell(DmBaseProject):
    """
    basisdatenebene für den verschnitt von koppel und gst-version
    """
    __tablename__ = '_tbl_alm_cut_koppel_aktuell_gstversion'

    id: Mapped[int] = mapped_column(primary_key=True)
    koppel_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_koppel.id"))
    gst_version_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst_version.id"))
    timestamp: Mapped[str]
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
                               srid=31259))

    rel_koppel: Mapped["DmKoppel"] = relationship(back_populates='rel_cut_koppel_gst')
    rel_gstversion: Mapped["DmGstVersion"] = relationship(back_populates='rel_cut_koppel_gst')

    # id = Column(Integer, primary_key=True)
    # komplex_id = Column(Integer, ForeignKey('a_alm_koppel.id'))
    # gst_version_id = Column(Integer, ForeignKey('a_alm_gst_version.id'))
    # timestamp = Column(String)
    # geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
    #                            srid=31259))

    # rel_koppel = relationship('DmKomplex',
    #                            back_populates="rel_cut_komplex_gstversion")
    # rel_gstversion = relationship('DmGstVersion',
    #                               back_populates="rel_cut_komplex_gstversion")

    @hybrid_property
    def cut_area(self):

        cc = to_shape(self.geometry).area

        # return func.ST_Area(self.geometry)
        return cc

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"id: {self.id}, " \
               f"koppel_id: {self.koppel_id}, " \
               f"gstversion_id:{self.gst_version_id})"


class DmErfassungsart(DmBaseProject):
    """
    Mapperklasse für die Erfassungsart einer Abgrenzung
    """
    __tablename__ = "_tbl_alm_erfassungsart"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    name_short: Mapped[str]

    rel_abgrenzung: Mapped["DmAbgrenzung"] = relationship(
        back_populates='rel_erfassungsart')

    def __repr__(self):
        return f"<DmErfassungsart(id: {self.id}, " \
               f"name: {self.name})>"


class DmGisLayer(DmBaseProject):
    """
    Basisdatenebene für gis_layer
    """
    __tablename__ = "_tbl_app_gis_layer"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    beschreibung = Column(String)
    table_name = Column(String)
    geometry_col = Column(String)
    uri = Column(String)
    provider = Column(String)
    layer_typ = Column(String)

    rel_gis_style = relationship('DmGisStyle', back_populates="rel_gis_layer")

    def __repr__(self):
        return f"<DmGisLayer(id: {self.id}, " \
               f"name: {self.name}, " \
               f"provider: {self.provider})>"


class DmGisLayerMenu(DmBaseProject):
    """
    basisdatenebene für menübäume, mit denen man layer auswählen und einfügen
    kann
    """
    __tablename__ = "_tbl_app_gis_layer_menu"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    parent_id = Column(Integer)
    name = Column(String)
    style_id = Column(Integer, ForeignKey('_tbl_app_gis_style.id'))
    sort = Column(String)

    rel_gis_style = relationship('DmGisStyle',
                                 back_populates='rel_gis_layer_menu')

    def __repr__(self):
        return f"<DmGisLayerMenu(id: {self.id}, " \
               f"parent_id: {self.parent_id}, " \
               f"name: {self.name})>"


class DmGisStyle(DmBaseProject):
    """
    basisdatenebene für gis_style
    """
    __tablename__ = "_tbl_app_gis_style"

    id = Column(Integer, primary_key=True)
    gis_layer_id = Column(Integer, ForeignKey('_tbl_app_gis_layer.id'))
    name = Column(String)
    background = Column(Boolean)
    qml_file = Column(String)
    dataform_modul = Column(String)
    dataform_class = Column(String)

    rel_gis_layer = relationship('DmGisLayer',
                                 back_populates="rel_gis_style",
                                 lazy='joined')
    rel_gis_scope_layer = relationship('DmGisScopeLayer',
                                       back_populates="rel_gis_style")
    rel_gis_style_layer_var = relationship('DmGisStyleLayerVar',
                                           back_populates='rel_gis_style',
                                           lazy='joined')
    rel_gis_layer_menu = relationship('DmGisLayerMenu',
                                      back_populates='rel_gis_style',
                                      lazy='joined')

    def __repr__(self):
        return f"<DmGisStyle(id: {self.id}, " \
               f"gis_layer_id: {self.gis_layer_id}, " \
               f"name: {self.name})>"


class DmGisStyleLayerVar(DmBaseProject):
    """
    basisdatenebene für layervariablen die je gis-style definiert werden
    können
    """
    __tablename__ = "_tbl_app_gis_style_layer_var"

    id = Column(Integer, primary_key=True)
    gis_style_id = Column(Integer, ForeignKey('_tbl_app_gis_style.id'))
    name = Column(String)  # name der variable (ohne führendes '@')
    value = Column(String)  # wert der variable
    code_value = Column(Boolean)  # True wenn 'value' ein code ist

    rel_gis_style = relationship('DmGisStyle',
                                 back_populates='rel_gis_style_layer_var')

    def __repr__(self):
        return f"<DmGisStyleLayerVar(id: {self.id}, " \
               f"gis_style_id: {self.gis_style_id}, " \
               f"name: {self.name})>"


class DmGisScope(DmBaseProject):
    """
    basisdatenebene für gis_scope
    """
    __tablename__ = "_tbl_app_gis_scope"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    rel_gis_scope_layer = relationship('DmGisScopeLayer',
                                       back_populates="rel_gis_scope")

    def __repr__(self):
        return f"<DmGisScope(id: {self.id}, " \
               f"name: {self.name})>"


class DmGisScopeLayer(DmBaseProject):
    """
    basisdatenebene für gis_scope_layer
    """
    __tablename__ = "_tbl_app_scope_layer"

    id = Column(Integer, primary_key=True)
    gis_scope_id = Column(Integer, ForeignKey('_tbl_app_gis_scope.id'))
    gis_style_id = Column(Integer, ForeignKey('_tbl_app_gis_style.id'))
    order = Column(Integer)
    background = Column(Boolean)
    baselayer = Column(Boolean)
    base_id_column = Column(String)
    feat_filt_expr = Column(String)
    add = Column(Boolean)

    rel_gis_scope = relationship('DmGisScope',
                                 back_populates="rel_gis_scope_layer",
                                 lazy='joined')
    rel_gis_style = relationship('DmGisStyle',
                                 back_populates="rel_gis_scope_layer",
                                 lazy='joined')

    def __repr__(self):
        return f"<DmGisScopeLayer(id: {self.id}, " \
               f"gis_scope_id: {self.gis_scope_id}, " \
               f"gis_style_id: {self.gis_style_id})>"


class DmGst(DmBaseProject):
    """
    alle grundstücke die aktuell in der DB verfügbar sind
    (alle bereits zugeordneten und die gst, die im gst-importverzeichis sind)
    """
    __tablename__ = '_tbl_alm_gst'

    id: Mapped[int] = mapped_column(primary_key=True)
    kg_gst: Mapped[str]
    kgnr: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_kg.kgnr"))
    gst: Mapped[str]

    """folgende Beziehungen sind 'child' Beziehungen"""
    # rel_alm_gst_version = relationship('DmGstVersion',
    #                                    back_populates="rel_alm_gst",
    #                                    cascade="all, delete, delete-orphan",
    #                                    passive_deletes=True)
    rel_alm_gst_version: Mapped[List["DmGstVersion"]] = relationship(
        back_populates="rel_alm_gst",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
        lazy='joined')

    # rel_gst_zuordnung = relationship('DmGstZuordnung',
    #                                  back_populates="rel_gst")
    rel_gst_zuordnung: Mapped[List["DmGstZuordnung"]] = relationship(
        back_populates="rel_gst")
    """"""

    rel_kat_gem: Mapped["DmKatGem"] = relationship(
        back_populates="rel_alm_gst",
        lazy='joined')

    @hybrid_property
    def gst_latest(self):
        return max(self.rel_alm_gst_version,
                   key=lambda x: x.rel_alm_gst_ez.datenstand) if self.rel_alm_gst_version else None

    # @gst_latest.expression
    # def gst_latest(cls):
    #     subq = (
    #         select(RelatedModel)
    #         .filter(RelatedModel.my_model_id == cls.id)
    #         .order_by(RelatedModel.version.desc())
    #         .limit(1)
    #         .scalar_subquery()
    #     )
    #     return subq

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"kg_gst: {self.kg_gst}, gst:{self.gst})>"


class DmGstAwbStatus(DmBaseProject):
    """
    alm- und weidebuch-status_id eines grundstückes
    """
    __tablename__ = '_tbl_alm_awb_status'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    description = Column(String)
    sort = Column(Integer)
    color_main = Column(String)

    rel_gst_zuordnung = relationship('DmGstZuordnung',
                                     back_populates='rel_awb_status')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"


class DmGstEigentuemer(DmBaseProject):
    """
    basisdatenebene für eigentuemer
    """
    __tablename__ = "_tbl_alm_gst_eigentuemer"

    id: Mapped[int] = mapped_column(primary_key=True)
    # ez_id = Column(Integer, ForeignKey('a_alm_gst_ez.id'))
    ez_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst_ez.id"))
    kg_ez: Mapped[int]
    anteil: Mapped[int]
    anteil_von: Mapped[int]
    name: Mapped[str]
    geb_dat: Mapped[str]
    adresse: Mapped[str]

    # rel_alm_gst_ez = relationship("DmGstEz",
    #                               back_populates="rel_alm_gst_eigentuemer")
    rel_alm_gst_ez: Mapped["DmGstEz"] = relationship(
        back_populates="rel_alm_gst_eigentuemer")

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, " \
               f"ez_id: {self.ez_id}, kg_ez:{self.kg_ez}, name: {self.name})"


class DmGstEz(DmBaseProject):
    """
    basisdatenebene für einlagezahlen (ez)
    """
    __tablename__ = "_tbl_alm_gst_ez"

    id: Mapped[int] = mapped_column(primary_key=True)
    # kgnr = Column(Integer, ForeignKey('a_sys_kg.kgnr'))
    kgnr: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_kg.kgnr"))

    ez: Mapped[int]
    kg_ez: Mapped[str]
    datenstand: Mapped[str]
    import_time: Mapped[str]

    # rel_alm_gst_version = relationship("DmGstVersion",
    #                                    back_populates="rel_alm_gst_ez")
    rel_alm_gst_version: Mapped[List["DmGstVersion"]] = relationship(
        back_populates="rel_alm_gst_ez")

    # rel_alm_gst_eigentuemer = relationship("DmGstEigentuemer",
    #                                        back_populates="rel_alm_gst_ez",
    #                                        cascade="all, delete-orphan")
    rel_alm_gst_eigentuemer: Mapped[List["DmGstEigentuemer"]] = relationship(
        back_populates="rel_alm_gst_ez",
        cascade="all, delete-orphan",
        lazy='joined')

    # rel_kat_gem = relationship("DmKatGem",
    #                            back_populates="rel_alm_gst_ez")
    rel_kat_gem: Mapped["DmKatGem"] = relationship(
        back_populates="rel_alm_gst_ez",
        lazy='joined')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"kgnr: {self.kgnr}, ez: {self.ez})>"


class DmGstNutzung(DmBaseProject):
    """
    basisdatenebene für die benützungsarten der gst
    """
    __tablename__ = "_tbl_alm_gst_nutzung"

    id: Mapped[int] = mapped_column(primary_key=True)
    # gst_version_id = Column(Integer, ForeignKey('a_alm_gst_version.id'))
    gst_version_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst_version.id"))
    banu_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_banu.id"))
    ba_id: Mapped[int]
    nu_id: Mapped[int]
    area: Mapped[int]

    # rel_alm_gst_version = relationship("DmGstVersion",
    #                                    back_populates="rel_alm_gst_nutzung")
    rel_alm_gst_version: Mapped["DmGstVersion"] = relationship(
        back_populates="rel_alm_gst_nutzung")

    rel_banu: Mapped["DmBanu"] = relationship(
        back_populates="rel_alm_gst_nutzung",
        lazy='joined')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"gst_version_id: {self.gst_version_id}, ba_id: {self.ba_id})"


class DmGstVersion(DmBaseProject):
    """
    die versionsabhängigen informationen der gst;
    ein jüngerer gst-import (= jüngerer datenstand) bedeutet z.B. eine neue
    version des gst
    """
    __tablename__ = '_tbl_alm_gst_version'

    id: Mapped[int] = mapped_column(primary_key=True)
    # gst_id = Column(Integer, ForeignKey('a_alm_gst.id', ondelete='CASCADE'))
    gst_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst.id", ondelete='CASCADE'))

    # ez_id = Column(Integer, ForeignKey('a_alm_gst_ez.id'))
    ez_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst_ez.id"))

    gk: Mapped[str]
    source_id: Mapped[int]
    import_time: Mapped[str]
    # geometry: Mapped[bytes]
    geometry: Mapped[object] = mapped_column(Geometry(geometry_type="MULTIPOLYGON",
                               srid=31259))
    """alte configuration"""
    # geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
    #                            srid=31259))
    """"""

    """'child' Beziehungen:"""
    # rel_alm_gst_nutzung = relationship('DmGstNutzung',
    #                                    back_populates="rel_alm_gst_version",
    #                                    cascade="all, delete-orphan")
    rel_alm_gst_nutzung: Mapped[List["DmGstNutzung"]] = relationship(
        back_populates="rel_alm_gst_version",
        cascade="all, delete-orphan",
        lazy='joined')

    # rel_cut_koppel_gst = relationship('DmCutKoppelGstAktuell',
    #                                           back_populates="rel_gstversion",
    #                                           cascade="all, delete, delete-orphan")
    rel_cut_koppel_gst: Mapped[List["DmCutKoppelGstAktuell"]] = relationship(
        back_populates="rel_gstversion",
        cascade="all, delete, delete-orphan",
        lazy='joined')
    """"""

    """'parent' Beziehungen:"""
    # rel_alm_gst = relationship('DmGst',
    #                            back_populates="rel_alm_gst_version")
    rel_alm_gst: Mapped["DmGst"] = relationship(
        back_populates="rel_alm_gst_version",
        lazy='immediate')

    # rel_alm_gst_ez = relationship('DmGstEz',
    #                               back_populates="rel_alm_gst_version")
    rel_alm_gst_ez: Mapped["DmGstEz"] = relationship(
        back_populates="rel_alm_gst_version",
        lazy='joined')
    """"""

    @hybrid_property
    # @property
    def gst_gis_area(self):

        # todo: use here 'self.geometry.ST_Area()' instead; but
        #  'mod_spatialite' must be enabled in SQLite-Db, or use PostGIS

        # aa = func.ST_Area(self.geometry)
        aa = to_shape(self.geometry).area  # float

        return aa

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, " \
               f"gst_id: {self.gst_id}, source_id:{self.source_id})"


class DmGstZuordnung(DmBaseProject):
    """
    zuordnung der grundstücke zu einem akt
    """
    __tablename__ = "_tbl_alm_gst_zuordnung"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_akt.id"))
    gst_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_gst.id"))
    awb_status_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_awb_status.id"))
    rechtsgrundlage_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_rechtsgrundlage.id"))

    anmerkung: Mapped[str]
    probleme: Mapped[str]
    aufgaben: Mapped[str]
    gb_wrong: Mapped[bool]
    awb_wrong: Mapped[bool]

    user_create: Mapped[str] = mapped_column(default=os.getlogin())
    time_create: Mapped[str] = mapped_column(default=datetime.now())
    user_edit: Mapped[str] = mapped_column(default=os.getlogin(),
                                           onupdate=os.getlogin())
    time_edit: Mapped[str] = mapped_column(default=datetime.now(),
                                           onupdate=datetime.now())

    # update = Column(DateTime, onupdate=datetime.now())
    # update_user = Column(String, onupdate=os.getlogin())

    """alle Beziehungen sind 'parent' Beziehungen"""
    # rel_akt = relationship('DmAkt',
    #                        back_populates='rel_gst_zuordnung')
    rel_akt: Mapped["DmAkt"] = relationship(
        back_populates="rel_gst_zuordnung",
        lazy='immediate')

    # rel_gst = relationship('DmGst',
    #                        back_populates='rel_gst_zuordnung')
    rel_gst: Mapped["DmGst"] = relationship(
        back_populates="rel_gst_zuordnung")

    # rel_awb_status = relationship('DmGstAwbStatus',
    #                               back_populates='rel_gst_zuordnung')
    rel_awb_status: Mapped["DmGstAwbStatus"] = relationship(
        back_populates="rel_gst_zuordnung",
        lazy='joined')

    # rel_rechtsgrundlage = relationship('DmRechtsgrundlage',
    #                                    back_populates='rel_gst_zuordnung')
    rel_rechtsgrundlage: Mapped["DmRechtsgrundlage"] = relationship(
        back_populates="rel_gst_zuordnung",
        lazy='joined')
    """"""

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"akt_id: {self.akt_id}, gst_id:{self.gst_id})>"


class DmGstZuordnungMain(DmBaseProject):
    """
    view mit den jüngsten gst die einem akt zugeordnet sind
    """
    __tablename__ = "_tbl_alm_gst_zuordnung_main"

    id = Column(Integer, primary_key=True)
    zuord_id = Column(Integer)
    kg_gst = Column(String)
    kgnr = Column(Integer)
    kg_name = Column(String)
    gst = Column(String)
    ez = Column(Integer)
    source_id = Column(Integer)
    zu_aw = Column(String)
    datenstand = Column(String)
    import_time = Column(String)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
                               srid=31259))

    def __repr__(self):
        return f"{self.__class__.__name__}(kg_gst: {self.kg_gst}, " \
               f"gst: {self.gst})"


# class DmInfoButton(DmBaseCommon, DmNonSpatialObject):
class DmInfoButton(DmBaseCommon):
    __tablename__ = '_tbl_info_button'

    id = Column(Integer, primary_key=True)
    btn = Column(String)
    title = Column(String)
    content = Column(String)

    def __repr__(self):
       return f"<<DmInfoButton(id='{self.id}', title='{self.title}')>>"


class DmKatGem(DmBaseProject):
    """
    liste der katastralgemeinden in nö
    """
    __tablename__ = "_tbl_alm_kg"

    kgnr: Mapped[int] = mapped_column(primary_key=True)
    kgname: Mapped[str]
    pgnr: Mapped[int]
    pgname: Mapped[str]
    pbnr: Mapped[int]
    pbname: Mapped[str]

    # rel_alm_gst_ez = relationship("DmGstEz",
    #                               back_populates="rel_kat_gem")
    rel_alm_gst_ez: Mapped["DmGstEz"] = relationship(
        back_populates="rel_kat_gem")

    rel_alm_gst: Mapped["DmGst"] = relationship(
        back_populates="rel_kat_gem")

    def __repr__(self):
        return f"<DmKatGem(kgnr: {self.kgnr}, kgname: {self.kgname}, " \
               f"pgname: {self.pgname})"


class DmAbgrenzung(DmBaseProject):
    """
    Mapperklasse für eine Abgrenzung der Alm/Weide;
    innerhalb eines Aktes können daher unterschiedliche Abgrenzungen angelegt
    werden (diese können sich unterscheiden in Jahr, Bearbeiter, Status, ...)
    """
    __tablename__ = "_tbl_alm_abgrenzung"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_akt.id"))
    # komplex_id: Mapped[int] = mapped_column(ForeignKey("a_alm_komplex.id"))
    jahr: Mapped[int]
    bearbeiter: Mapped[str]
    erfassungsart_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_erfassungsart.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_abgrenzung_status.id"))
    awb: Mapped[bool]
    bezeichnung: Mapped[str]
    anmerkung: Mapped[str]
    inaktiv: Mapped[bool]

    rel_akt: Mapped["DmAkt"] = relationship(back_populates='rel_abgrenzung')
    rel_komplex: Mapped[List["DmKomplex"]] = relationship(back_populates='rel_abgrenzung',
                                                         cascade="all, delete, delete-orphan")
    # rel_koppel: Mapped[List["DmKoppel"]] = relationship(back_populates='rel_komplex_version')

    rel_erfassungsart: Mapped["DmErfassungsart"] = relationship(back_populates='rel_abgrenzung')
    rel_status: Mapped["DmAbgrenzungStatus"] = relationship(back_populates='rel_abgrenzung')

    def __repr__(self):
        return f"<DmAbgrenzung(id: {self.id}, " \
               f"akt_id: {self.akt_id}, " \
               f"jahr: {self.jahr})>"


class DmAbgrenzungStatus(DmBaseProject):
    """
    Mapperklasse für den Status einer Abgrenzung
    """
    __tablename__ = "_tbl_alm_abgrenzung_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    name_short: Mapped[str]

    rel_abgrenzung: Mapped["DmAbgrenzung"] = relationship(
        back_populates='rel_status')

    def __repr__(self):
        return f"<DmAbgrenzungStatus(id: {self.id}, " \
               f"name: {self.name})>"


class DmKomplex(DmBaseProject):
    """
    Mapperklasse für die Komplexe eines Aktes (entsprechend einer Abgrenzung)
    """
    __tablename__ = "_tbl_alm_komplex"

    id: Mapped[int] = mapped_column(primary_key=True)
    abgrenzung_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_abgrenzung.id"))
    komplex_name_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_komplex_name.id"))

    rel_koppel: Mapped[List["DmKoppel"]] = relationship(back_populates='rel_komplex',
                                                       cascade="all, delete, delete-orphan")
    rel_abgrenzung: Mapped["DmAbgrenzung"] = relationship(back_populates='rel_komplex')
    rel_komplex_name: Mapped["DmKomplexName"] = relationship(back_populates='rel_komplex')

    def __repr__(self):
        return f"<DmKomplex(id: {self.id}, " \
               f"abgrenzung_id: {self.abgrenzung_id}, " \
               f"komplex_name_id: {self.komplex_name_id})>"


class DmKomplexName(DmBaseProject):
    """
    Mapperklasse für die Komplexnamen eines Aktes
    """
    __tablename__ = "_tbl_alm_komplex_name"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey('_tbl_alm_akt.id'))
    nr: Mapped[int]
    name: Mapped[str]
    anmerkung: Mapped[str]
    inaktiv: Mapped[bool]

    rel_akt: Mapped["DmAkt"] = relationship(back_populates='rel_komplex_name')
    # rel_komplex_version: Mapped[List["DmKomplexVersion"]] = relationship(back_populates="rel_komplex")
    rel_komplex: Mapped[List[DmKomplex]] = relationship(back_populates='rel_komplex_name')

    def __repr__(self):
        return f"<DmKomplexName(id: {self.id}, " \
               f"akt_id: {self.akt_id}, " \
               f"name: {self.name})>"

class DmKontakt(DmBaseProject, DmNonSpatialObject):
# class DmKontakt(DmBaseProject):
    __tablename__ = '_tbl_alm_kontakt'

    """class with self-relation!"""
    # id: Mapped[int] = mapped_column(primary_key=True)
    # id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    """"""

    id: Mapped[UUID] = mapped_column(primary_key=True,
                                       default=uuid4)
    """or 'id' is a integer """
    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    """"""
    type_id: Mapped[int] = mapped_column(ForeignKey('_tbl_alm_kontakt_type.id'),
                                         nullable=True)
    gem_type_id: Mapped[int] = mapped_column(ForeignKey('_tbl_alm_kontakt_gem_type.id'),
                                             nullable=True)
    """self-relation to id!!"""
    vertreter_id: Mapped[UUID] = mapped_column(ForeignKey("_tbl_alm_kontakt.id"),
                                              nullable=True)
    """"""

    nachname: Mapped[str] = mapped_column(nullable=True)
    vorname: Mapped[str] = mapped_column(nullable=True)
    strasse: Mapped[str] = mapped_column(nullable=True)
    plz: Mapped[str] = mapped_column(nullable=True)
    ort: Mapped[str] = mapped_column(nullable=True)
    telefon1: Mapped[str] = mapped_column(nullable=True)
    telefon2: Mapped[str] = mapped_column(nullable=True)
    telefon3: Mapped[str] = mapped_column(nullable=True)
    mail1: Mapped[str] = mapped_column(nullable=True)
    mail2: Mapped[str] = mapped_column(nullable=True)
    mail3: Mapped[str] = mapped_column(nullable=True)

    anm: Mapped[str] = mapped_column(nullable=True)

    blank_value: Mapped[bool] = mapped_column(default=0)
    inactive: Mapped[bool] = mapped_column(default=0)
    not_delete: Mapped[bool] = mapped_column(default=0)

    user_edit: Mapped[str] = mapped_column(default=os.getlogin(),
                                           onupdate=os.getlogin())
    time_edit: Mapped[str] = mapped_column(default=datetime.now(),
                                           onupdate=datetime.now())

    rel_type: Mapped['DmKontaktType'] = relationship()
    rel_gem_type: Mapped['DmKontaktGemTyp'] = relationship(lazy="joined")

    # children = relationship("DmKontakt", back_populates="rel_vertreter")
    children: Mapped[List[
        "DmKontakt"]] = relationship(back_populates="rel_vertreter")
    rel_vertreter = relationship("DmKontakt", lazy="joined", join_depth=1,
                             remote_side=[id])

    rel_akt: Mapped[List["DmAkt"]] = relationship(back_populates="rel_bewirtschafter")

    # __mapper_args__ = {
    #     'polymorphic_on': type_id
    # }

    @hybrid_property
    def name(self):

        name = ''

        if self.nachname != '':
            name += self.nachname

        if self.vorname != '':
            name += ' '
            name += self.vorname

        return name

    @hybrid_property
    def adresse(self):

        adresse = ''

        if str(self.plz) != '':
            adresse += str(self.plz)

        if self.ort != '':
            adresse += ' '
            adresse += self.ort

        if self.strasse != '':
            adresse += ', '
            adresse += self.strasse

        return adresse

    @hybrid_property
    def telefon_all(self):

        telfon_list = []

        if self.telefon1 != '':
            telfon_list.append(self.telefon1)

        if self.telefon2 != '':
            telfon_list.append(self.telefon2)

        if self.telefon3 != '':
            telfon_list.append(self.telefon3)

        telefon_all = ", ".join(str(t) for t in telfon_list)

        return telefon_all

    @hybrid_property
    def mail_all(self):

        mail_list = []

        if self.mail1 != '':
            mail_list.append(self.mail1)

        if self.mail2 != '':
            mail_list.append(self.mail2)

        if self.mail3 != '':
            mail_list.append(self.mail3)

        mail_all = ", ".join(str(m) for m in mail_list)

        return mail_all

    @hybrid_property
    def name(self):

        name = ''

        try:
            if self.nachname != '':
                name += self.nachname

            if self.vorname != '':
                name += ' '
                name += self.vorname
        except:
            pass

        return name

    @hybrid_property
    def adresse(self):

        adresse = ''

        if str(self.plz) != '':
            adresse += str(self.plz)

        # print(f'self.ort: {self.ort}')

        if self.ort != '' and self.ort is not None:
            adresse += ' '
            adresse += self.ort

        if self.strasse != '' and self.strasse is not None:
            adresse += ', '
            adresse += self.strasse

        return adresse

    @hybrid_property
    def telefon_all(self):

        telfon_list = []

        if self.telefon1 != '':
            telfon_list.append(self.telefon1)

        if self.telefon2 != '':
            telfon_list.append(self.telefon2)

        if self.telefon3 != '':
            telfon_list.append(self.telefon3)

        telefon_all = ", ".join(str(t) for t in telfon_list)

        return telefon_all

    @hybrid_property
    def mail_all(self):

        mail_list = []

        if self.mail1 != '':
            mail_list.append(self.mail1)

        if self.mail2 != '':
            mail_list.append(self.mail2)

        if self.mail3 != '':
            mail_list.append(self.mail3)

        mail_all = ", ".join(str(m) for m in mail_list)

        return mail_all

    def __init__(self):  # set default values

        # self.type_id = 0

        self.blank_value = 0
        self.inactive = 0
        self.not_delete = 0

    def __repr__(self):
       return f"<DmKontakt(id={self.id}, nachname='{self.nachname}')>"


class DmKontaktEinzel(DmKontakt):

    __mapper_args__ = {
        'polymorphic_identity': 0,
    }


class DmKontaktGem(DmKontakt):

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }


class DmKontaktType(DmBaseProject):
    """
    tabelle für die kontakt-typen (v.a. Einzel- oder Gemeinschaftskontakt
    """
    __tablename__ = '_tbl_alm_kontakt_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_id: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    name_short: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    sort: Mapped[int] = mapped_column(nullable=True)
    color_main: Mapped[str] = mapped_column(nullable=True)
    icon_01: Mapped[str] = mapped_column(nullable=True)
    shortcut_01: Mapped[str] = mapped_column(nullable=True)
    module: Mapped[str] = mapped_column(nullable=True)
    type_class: Mapped[str] = mapped_column(nullable=True)
    dmi_class: Mapped[str] = mapped_column(nullable=True)
    value: Mapped[str] = mapped_column(nullable=True)

    blank_value: Mapped[bool] = mapped_column(nullable=True)
    inactive: Mapped[bool] = mapped_column(nullable=True)
    not_delete: Mapped[bool] = mapped_column(nullable=True)
    sys_data: Mapped[bool] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<{self.__class__}(id={self.id}," \
               f" parent_id={self.parent_id}, name={self.name})>"


class DmKontaktGemTyp(DmBaseProject):
    """
    tabelle für die unterschiedlichen typen eines Gemeinschaftskontaktes

    """
    __tablename__ = '_tbl_alm_kontakt_gem_type'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=True)
    name_short: Mapped[str] = mapped_column(nullable=True)

    color: Mapped[str] = mapped_column(nullable=True)
    sort: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self):
       return (f"<DmKontaktGemTyp(id={self.id}, "
               f"name='{self.name}, "
               f"name_short='{self.name_short}')>")

class DmKoppel(DmBaseProject):
    """
    Datenebene für Koppeln
    """
    __tablename__ = "_tbl_alm_koppel"

    id: Mapped[int] = mapped_column(primary_key=True)
    komplex_id: Mapped[int] = mapped_column(ForeignKey("_tbl_alm_komplex.id"))
    # komplex_version_id: Mapped[int] = mapped_column(ForeignKey("a_alm_komplex_version.id"))
    nr: Mapped[int]
    name: Mapped[str]
    nicht_weide: Mapped[int]  # 0 = False und 1 = True
    bearbeiter: Mapped[str]
    seehoehe: Mapped[int]
    domes_id: Mapped[int]
    heuertrag_ha: Mapped[int]
    anmerkung: Mapped[str]
    # geometry: Mapped[Geometry(geometry_type="POLYGON", srid=31259)]
    geometry = Column(Geometry(geometry_type="POLYGON", srid=31259))
    # geometry: Mapped[str]

    rel_komplex: Mapped["DmKomplex"] = relationship(back_populates='rel_koppel')
    rel_cut_koppel_gst: Mapped[List["DmCutKoppelGstAktuell"]] = relationship(
        back_populates='rel_koppel',
        cascade="all, delete, delete-orphan")

    @hybrid_property
    # @property
    def koppel_area(self):

        # aa = func.ST_Area(self.geometry)
        if isinstance(self.geometry, WKBElement):
            """standard beim auslesen aus der db"""
            aa = to_shape(self.geometry).area  # float
            """"""
        else:
            """notwendig für neu erzeugte koppeln, die noch nicht
            in der db sind"""
            geom_wkt = self.geometry
            geom_new = QgsGeometry()
            geom = geom_new.fromWkt(geom_wkt)
            aa = geom.area()
            """"""

        return aa

    def __repr__(self):
        return f"<DmKoppel(id: {self.id}, " \
               f"komplex_id: {self.komplex_id}, " \
               f"nr: {self.nr})>"


class DmRechtsgrundlage(DmBaseProject):
    """
    basisdatenebene für die rechstgrundlage der grundstücksbewirtschaftung;
    d.h. auf grund welcher rechtlichen situation ein grundstück beweidet wird;
    """
    __tablename__ = '_tbl_alm_rechtsgrundlage'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    description = Column(String)
    sort = Column(Integer)
    color_main = Column(String)

    rel_gst_zuordnung = relationship('DmGstZuordnung',
                                     back_populates='rel_rechtsgrundlage')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"name='{self.name}')>"


class DmSettings(DmBaseProject):
    """
    Einstellungen die vom Benutzer verändert werden können
    """
    __tablename__ = '_tbl_settings'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    value: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"code='{self.code}, name='{self.name}')>"

class DmSys(DmBaseProject):
    """
    Systemwerte
    """
    __tablename__ = '_tbl_qga_sys'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"key='{self.key}, value='{self.value}')>"
