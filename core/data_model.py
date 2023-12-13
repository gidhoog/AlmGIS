import os
from datetime import datetime
from typing import List

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BAkt(Base):
    """
    basisdatenebene für akte
    """
    __tablename__ = "a_alm_akt"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    alias = Column(String)
    az = Column(Integer)
    bearbeitungsstatus_id = Column(Integer, ForeignKey('a_alm_bearbeitungsstatus.id'))
    alm_bnr = Column(Integer)
    anm = Column(String)
    stz = Column(String)

    rel_bearbeitungsstatus = relationship('BBearbeitungsstatus')
    rel_gst_zuordnung = relationship('BGstZuordnung', back_populates='rel_akt')
    rel_komplex = relationship('BKomplex', back_populates='rel_akt')
    rel_komplex_version = relationship('BKomplexVersion', back_populates='rel_akt')

    def __repr__(self):
        return "<BAkt(id='%s', name='%s', az='%s')>" % (
                            self.id, self.name, self.az)


class BBanu(Base):
    """
    Datenebene für den banu-Wert
    """
    __tablename__ = 'a_sys_banu'

    id: Mapped[int] = mapped_column(primary_key=True)
    ba_id: Mapped[int]
    ba_name: Mapped[str]
    ba_name_short: Mapped[str]
    nu_id: Mapped[int]
    nu_name: Mapped[str]
    nu_name_short: Mapped[str]
    symbol: Mapped[int]

    rel_alm_gst_nutzung: Mapped["BGstNutzung"] = relationship(
        back_populates='rel_banu')


class BBearbeitungsstatus(Base):
    """
    basisdatenebene für den bearbeitungsstatus
    """
    __tablename__ = 'a_alm_bearbeitungsstatus'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_short = Column(String)
    sort = Column(Integer)

    def __repr__(self):
        return f"<BBearbeitungsstatus(id={self.id}, name='{self.name}')>"


class BCutKoppelGstAktuell(Base):
    """
    basisdatenebene für den verschnitt von koppel und gst-version
    """
    __tablename__ = 'a_cut_koppel_aktuell_gstversion'

    id: Mapped[int] = mapped_column(primary_key=True)
    koppel_id: Mapped[int] = mapped_column(ForeignKey("a_alm_koppel.id"))
    gst_version_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst_version.id"))
    timestamp: Mapped[str]
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
                               srid=31259))

    rel_koppel: Mapped["BKoppel"] = relationship(back_populates='rel_cut_koppel_gst')
    rel_gstversion: Mapped["BGstVersion"] = relationship(back_populates='rel_cut_koppel_gst')

    # id = Column(Integer, primary_key=True)
    # komplex_id = Column(Integer, ForeignKey('a_alm_koppel.id'))
    # gst_version_id = Column(Integer, ForeignKey('a_alm_gst_version.id'))
    # timestamp = Column(String)
    # geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
    #                            srid=31259))

    # rel_koppel = relationship('BKomplex',
    #                            back_populates="rel_cut_komplex_gstversion")
    # rel_gstversion = relationship('BGstVersion',
    #                               back_populates="rel_cut_komplex_gstversion")

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"id: {self.id}, " \
               f"koppel_id: {self.koppel_id}, " \
               f"gstversion_id:{self.gst_version_id})"


class BGisLayer(Base):
    """
    Basisdatenebene für gis_layer
    """
    __tablename__ = "a_gis_layer"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    beschreibung = Column(String)
    table_name = Column(String)
    geometry_col = Column(String)
    uri = Column(String)
    provider = Column(String)
    layer_typ = Column(String)

    rel_gis_style = relationship('BGisStyle', back_populates="rel_gis_layer")

    def __repr__(self):
        return f"<BGisLayer(id: {self.id}, " \
               f"name: {self.name}, " \
               f"provider: {self.provider})>"


class BGisLayerMenu(Base):
    """
    basisdatenebene für menübäume, mit denen man layer auswählen und einfügen
    kann
    """
    __tablename__ = "a_gis_layer_menu"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    parent_id = Column(Integer)
    name = Column(String)
    style_id = Column(Integer, ForeignKey('a_gis_style.id'))
    sort = Column(String)

    rel_gis_style = relationship('BGisStyle',
                                 back_populates='rel_gis_layer_menu')

    def __repr__(self):
        return f"<BGisLayerMenu(id: {self.id}, " \
               f"parent_id: {self.parent_id}, " \
               f"name: {self.name})>"


class BGisStyle(Base):
    """
    basisdatenebene für gis_style
    """
    __tablename__ = "a_gis_style"

    id = Column(Integer, primary_key=True)
    gis_layer_id = Column(Integer, ForeignKey('a_gis_layer.id'))
    name = Column(String)
    background = Column(Boolean)
    qml_file = Column(String)
    dataform_modul = Column(String)
    dataform_class = Column(String)

    rel_gis_layer = relationship('BGisLayer',
                                 back_populates="rel_gis_style",
                                 lazy='joined')
    rel_gis_scope_layer = relationship('BGisScopeLayer',
                                       back_populates="rel_gis_style")
    rel_gis_style_layer_var = relationship('BGisStyleLayerVar',
                                           back_populates='rel_gis_style',
                                           lazy='joined')
    rel_gis_layer_menu = relationship('BGisLayerMenu',
                                      back_populates='rel_gis_style',
                                      lazy='joined')

    def __repr__(self):
        return f"<BGisStyle(id: {self.id}, " \
               f"gis_layer_id: {self.gis_layer_id}, " \
               f"name: {self.name})>"


class BGisStyleLayerVar(Base):
    """
    basisdatenebene für layervariablen die je gis-style definiert werden
    können
    """
    __tablename__ = "a_gis_style_layer_var"

    id = Column(Integer, primary_key=True)
    gis_style_id = Column(Integer, ForeignKey('a_gis_style.id'))
    name = Column(String)  # name der variable (ohne führendes '@')
    value = Column(String)  # wert der variable
    code_value = Column(Boolean)  # True wenn 'value' ein code ist

    rel_gis_style = relationship('BGisStyle',
                                 back_populates='rel_gis_style_layer_var')

    def __repr__(self):
        return f"<BGisStyleLayerVar(id: {self.id}, " \
               f"gis_style_id: {self.gis_style_id}, " \
               f"name: {self.name})>"


class BGisScope(Base):
    """
    basisdatenebene für gis_scope
    """
    __tablename__ = "a_gis_scope"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    rel_gis_scope_layer = relationship('BGisScopeLayer',
                                       back_populates="rel_gis_scope")

    def __repr__(self):
        return f"<BGisScope(id: {self.id}, " \
               f"name: {self.name})>"


class BGisScopeLayer(Base):
    """
    basisdatenebene für gis_scope_layer
    """
    __tablename__ = "a_gis_scope_layer"

    id = Column(Integer, primary_key=True)
    gis_scope_id = Column(Integer, ForeignKey('a_gis_scope.id'))
    gis_style_id = Column(Integer, ForeignKey('a_gis_style.id'))
    order = Column(Integer)
    background = Column(Boolean)
    baselayer = Column(Boolean)
    base_id_column = Column(String)
    feat_filt_expr = Column(String)
    add = Column(Boolean)

    rel_gis_scope = relationship('BGisScope',
                                 back_populates="rel_gis_scope_layer",
                                 lazy='joined')
    rel_gis_style = relationship('BGisStyle',
                                 back_populates="rel_gis_scope_layer",
                                 lazy='joined')

    def __repr__(self):
        return f"<BGisScopeLayer(id: {self.id}, " \
               f"gis_scope_id: {self.gis_scope_id}, " \
               f"gis_style_id: {self.gis_style_id})>"


class BGst(Base):
    """
    alle grundstücke die aktuell in der DB verfügbar sind
    (alle bereits zugeordneten und die gst, die im gdb-importverzeichis sind)
    """
    __tablename__ = 'a_alm_gst'

    id: Mapped[int] = mapped_column(primary_key=True)
    kg_gst: Mapped[str]
    kgnr: Mapped[int] = mapped_column(ForeignKey("a_sys_kg.kgnr"))
    gst: Mapped[str]

    """folgende Beziehungen sind 'child' Beziehungen"""
    # rel_alm_gst_version = relationship('BGstVersion',
    #                                    back_populates="rel_alm_gst",
    #                                    cascade="all, delete, delete-orphan",
    #                                    passive_deletes=True)
    rel_alm_gst_version: Mapped[List["BGstVersion"]] = relationship(
        back_populates="rel_alm_gst",
        cascade="all, delete, delete-orphan",
        passive_deletes=True)

    # rel_gst_zuordnung = relationship('BGstZuordnung',
    #                                  back_populates="rel_gst")
    rel_gst_zuordnung: Mapped[List["BGstZuordnung"]] = relationship(
        back_populates="rel_gst")
    """"""

    rel_kat_gem: Mapped["BKatGem"] = relationship(
        back_populates="rel_alm_gst")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"kg_gst: {self.kg_gst}, gst:{self.gst})>"


class BGstAwbStatus(Base):
    """
    alm- und weidebuch-status eines grundstückes
    """
    __tablename__ = 'a_alm_awb_status'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    description = Column(String)
    sort = Column(Integer)
    color_main = Column(String)

    rel_gst_zuordnung = relationship('BGstZuordnung',
                                     back_populates='rel_awb_status')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"


class BGstEigentuemer(Base):
    """
    basisdatenebene für eigentuemer
    """
    __tablename__ = "a_alm_gst_eigentuemer"

    id: Mapped[int] = mapped_column(primary_key=True)
    # ez_id = Column(Integer, ForeignKey('a_alm_gst_ez.id'))
    ez_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst_ez.id"))
    kg_ez: Mapped[int]
    anteil: Mapped[int]
    anteil_von: Mapped[int]
    name: Mapped[str]
    geb_dat: Mapped[str]
    adresse: Mapped[str]

    # rel_alm_gst_ez = relationship("BGstEz",
    #                               back_populates="rel_alm_gst_eigentuemer")
    rel_alm_gst_ez: Mapped["BGstEz"] = relationship(
        back_populates="rel_alm_gst_eigentuemer")

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, " \
               f"ez_id: {self.ez_id}, kg_ez:{self.kg_ez}, name: {self.name})"


class BGstEz(Base):
    """
    basisdatenebene für einlagezahlen (ez)
    """
    __tablename__ = "a_alm_gst_ez"

    id: Mapped[int] = mapped_column(primary_key=True)
    # kgnr = Column(Integer, ForeignKey('a_sys_kg.kgnr'))
    kgnr: Mapped[int] = mapped_column(ForeignKey("a_sys_kg.kgnr"))

    ez: Mapped[int]
    kg_ez: Mapped[str]
    datenstand: Mapped[str]
    import_time: Mapped[str]

    # rel_alm_gst_version = relationship("BGstVersion",
    #                                    back_populates="rel_alm_gst_ez")
    rel_alm_gst_version: Mapped[List["BGstVersion"]] = relationship(
        back_populates="rel_alm_gst_ez")

    # rel_alm_gst_eigentuemer = relationship("BGstEigentuemer",
    #                                        back_populates="rel_alm_gst_ez",
    #                                        cascade="all, delete-orphan")
    rel_alm_gst_eigentuemer: Mapped[List["BGstEigentuemer"]] = relationship(
        back_populates="rel_alm_gst_ez",
        cascade="all, delete-orphan")

    # rel_kat_gem = relationship("BKatGem",
    #                            back_populates="rel_alm_gst_ez")
    rel_kat_gem: Mapped["BKatGem"] = relationship(
        back_populates="rel_alm_gst_ez")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"kgnr: {self.kgnr}, ez: {self.ez})>"


class BGstNutzung(Base):
    """
    basisdatenebene für die benützungsarten der gst
    """
    __tablename__ = "a_alm_gst_nutzung"

    id: Mapped[int] = mapped_column(primary_key=True)
    # gst_version_id = Column(Integer, ForeignKey('a_alm_gst_version.id'))
    gst_version_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst_version.id"))
    banu_id: Mapped[int] = mapped_column(ForeignKey("a_sys_banu.id"))
    ba_id: Mapped[int]
    nu_id: Mapped[int]
    area: Mapped[int]

    # rel_alm_gst_version = relationship("BGstVersion",
    #                                    back_populates="rel_alm_gst_nutzung")
    rel_alm_gst_version: Mapped["BGstVersion"] = relationship(
        back_populates="rel_alm_gst_nutzung")

    rel_banu: Mapped["BBanu"] = relationship(
        back_populates="rel_alm_gst_nutzung")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"gst_version_id: {self.gst_version_id}, ba_id: {self.ba_id})"


class BGstVersion(Base):
    """
    die versionsabhängigen informationen der gst;
    ein jüngerer gdb-import (= jüngerer datenstand) bedeutet z.B. eine neue
    version des gst
    """
    __tablename__ = 'a_alm_gst_version'

    id: Mapped[int] = mapped_column(primary_key=True)
    # gst_id = Column(Integer, ForeignKey('a_alm_gst.id', ondelete='CASCADE'))
    gst_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst.id", ondelete='CASCADE'))

    # ez_id = Column(Integer, ForeignKey('a_alm_gst_ez.id'))
    ez_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst_ez.id"))

    gk: Mapped[str]
    source_id: Mapped[int]
    import_time: Mapped[str]
    geometry: Mapped[object] = mapped_column(Geometry(geometry_type="MULTIPOLYGON",
                               srid=31259))
    """alte configuration"""
    # geometry = Column(Geometry(geometry_type="MULTIPOLYGON",
    #                            srid=31259))
    """"""

    """'child' Beziehungen:"""
    # rel_alm_gst_nutzung = relationship('BGstNutzung',
    #                                    back_populates="rel_alm_gst_version",
    #                                    cascade="all, delete-orphan")
    rel_alm_gst_nutzung: Mapped[List["BGstNutzung"]] = relationship(
        back_populates="rel_alm_gst_version",
        cascade="all, delete-orphan")

    # rel_cut_koppel_gst = relationship('BCutKoppelGstAktuell',
    #                                           back_populates="rel_gstversion",
    #                                           cascade="all, delete, delete-orphan")
    rel_cut_koppel_gst: Mapped[List["BCutKoppelGstAktuell"]] = relationship(
        back_populates="rel_gstversion",
        cascade="all, delete, delete-orphan")
    """"""

    """'parent' Beziehungen:"""
    # rel_alm_gst = relationship('BGst',
    #                            back_populates="rel_alm_gst_version")
    rel_alm_gst: Mapped["BGst"] = relationship(
        back_populates="rel_alm_gst_version")

    # rel_alm_gst_ez = relationship('BGstEz',
    #                               back_populates="rel_alm_gst_version")
    rel_alm_gst_ez: Mapped["BGstEz"] = relationship(
        back_populates="rel_alm_gst_version")
    """"""


    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, " \
               f"gst_id: {self.gst_id}, source_id:{self.source_id})"


class BGstZuordnung(Base):
    """
    zuordnung der grundstücke zu einem akt
    """
    __tablename__ = "a_alm_gst_zuordnung"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey("a_alm_akt.id"))
    gst_id: Mapped[int] = mapped_column(ForeignKey("a_alm_gst.id"))
    awb_status_id: Mapped[int] = mapped_column(ForeignKey("a_alm_awb_status.id"))
    rechtsgrundlage_id: Mapped[int] = mapped_column(ForeignKey("a_alm_rechtsgrundlage.id"))

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
    # rel_akt = relationship('BAkt',
    #                        back_populates='rel_gst_zuordnung')
    rel_akt: Mapped["BAkt"] = relationship(back_populates="rel_gst_zuordnung")

    # rel_gst = relationship('BGst',
    #                        back_populates='rel_gst_zuordnung')
    rel_gst: Mapped["BGst"] = relationship(back_populates="rel_gst_zuordnung")

    # rel_awb_status = relationship('BGstAwbStatus',
    #                               back_populates='rel_gst_zuordnung')
    rel_awb_status: Mapped["BGstAwbStatus"] = relationship(back_populates="rel_gst_zuordnung")

    # rel_rechtsgrundlage = relationship('BRechtsgrundlage',
    #                                    back_populates='rel_gst_zuordnung')
    rel_rechtsgrundlage: Mapped["BRechtsgrundlage"] = relationship(back_populates="rel_gst_zuordnung")
    """"""

    def __repr__(self):
        return f"<{self.__class__.__name__}(id: {self.id}, " \
               f"akt_id: {self.akt_id}, gst_id:{self.gst_id})>"


class BGstZuordnungMain(Base):
    """
    view mit den jüngsten gst die einem akt zugeordnet sind
    """
    __tablename__ = "v_gst_zuordnung_main"

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


class BKatGem(Base):
    """
    liste der katastralgemeinden in nö
    """
    __tablename__ = "a_sys_kg"

    kgnr: Mapped[int] = mapped_column(primary_key=True)
    kgname: Mapped[str]
    pgnr: Mapped[int]
    pgname: Mapped[str]
    pbnr: Mapped[int]
    pbname: Mapped[str]

    # rel_alm_gst_ez = relationship("BGstEz",
    #                               back_populates="rel_kat_gem")
    rel_alm_gst_ez: Mapped["BGstEz"] = relationship(
        back_populates="rel_kat_gem")

    rel_alm_gst: Mapped["BGst"] = relationship(
        back_populates="rel_kat_gem")

    def __repr__(self):
        return f"<BKatGem(kgnr: {self.kgnr}, kgname: {self.kgname}, " \
               f"pgname: {self.pgname})"


class BKomplex(Base):
    """
    basisdatenebene für komplexe (= eigenständige weideobjekte);
    je akt kann es mehrere komplexe geben
    """
    __tablename__ = "a_alm_komplex"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey('a_alm_akt.id'))
    nr: Mapped[int]
    name: Mapped[str]
    anmerkung: Mapped[str]
    inaktiv: Mapped[bool]

    rel_akt: Mapped["BAkt"] = relationship(back_populates='rel_komplex')
    rel_komplex_version: Mapped[List["BKomplexVersion"]] = relationship(back_populates="rel_komplex")

    def __repr__(self):
        return f"<BKomplex(id: {self.id}, " \
               f"akt_id: {self.akt_id}, " \
               f"name: {self.name})>"


class BKomplexVersion(Base):
    """
    Datenebene für unterschiedliche Versionen eines Komplexes (Jahr,
    Planungsversion, ...)
    """
    __tablename__ = "a_alm_komplex_version"

    id: Mapped[int] = mapped_column(primary_key=True)
    akt_id: Mapped[int] = mapped_column(ForeignKey("a_alm_akt.id"))
    komplex_id: Mapped[int] = mapped_column(ForeignKey("a_alm_komplex.id"))
    jahr: Mapped[int]
    bearbeiter: Mapped[str]
    erfassungsart_id: Mapped[int]
    version_id: Mapped[int]
    anmerkung: Mapped[str]
    inaktiv: Mapped[bool]

    rel_akt: Mapped["BAkt"] = relationship(back_populates='rel_komplex_version')
    rel_komplex: Mapped["BKomplex"] = relationship(back_populates='rel_komplex_version')
    rel_koppel: Mapped[List["BKoppel"]] = relationship(back_populates='rel_komplex_version')

    def __repr__(self):
        return f"<BKomplexVersion(id: {self.id}, " \
               f"komplex_id: {self.komplex_id}, " \
               f"jahr: {self.jahr})>"


class BKoppel(Base):
    """
    Datenebene für Koppeln
    """
    __tablename__ = "a_alm_koppel"

    id: Mapped[int] = mapped_column(primary_key=True)
    komplex_version_id: Mapped[int] = mapped_column(ForeignKey("a_alm_komplex_version.id"))
    nr: Mapped[int]
    name: Mapped[str]
    nicht_weide: Mapped[bool]
    bearbeiter: Mapped[str]
    seehoehe: Mapped[int]
    domes_id: Mapped[int]
    heuertrag_ha: Mapped[int]
    anmerkung: Mapped[str]
    # geometry: Mapped[Geometry(geometry_type="POLYGON", srid=31259)]
    geometry = Column(Geometry(geometry_type="POLYGON", srid=31259))

    rel_komplex_version: Mapped["BKomplexVersion"] = relationship(back_populates='rel_koppel')
    rel_cut_koppel_gst: Mapped["BCutKoppelGstAktuell"] = relationship(back_populates='rel_koppel')

    def __repr__(self):
        return f"<BKoppel(id: {self.id}, " \
               f"komplex_version_id: {self.komplex_version_id}, " \
               f"nr: {self.nr})>"


class BRechtsgrundlage(Base):
    """
    basisdatenebene für die rechstgrundlage der grundstücksbewirtschaftung;
    d.h. auf grund welcher rechtlichen situation ein grundstück beweidet wird;
    """
    __tablename__ = 'a_alm_rechtsgrundlage'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    description = Column(String)
    sort = Column(Integer)
    color_main = Column(String)

    rel_gst_zuordnung = relationship('BGstZuordnung',
                                     back_populates='rel_rechtsgrundlage')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"name='{self.name}')>"


class BSettings(Base):
    """
    Einstellungen die vom Benutzer verändert werden können
    """
    __tablename__ = 'a_sys_settings'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    name: Mapped[str]
    description: Mapped[str]
    value: Mapped[str]

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"code='{self.code}, name='{self.name}')>"

class BSys(Base):
    """
    Systemwerte
    """
    __tablename__ = 'a_alm_sys'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, " \
               f"key='{self.key}, value='{self.value}')>"
