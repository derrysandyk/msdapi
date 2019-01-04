import os
from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.oracle import NUMBER, TIMESTAMP, VARCHAR2, CLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
m_sparepart_vin = os.environ.get('m_sparepart_vin', 'm_sparepart_vin')
# MSD_TB_VIN = os.environ.get('MSD_TB_VIN', 'MSD_TB_VIN')
# MSD_TB_ABBREVIATION = os.environ.get('MSD_TB_ABBREVIATION', 'MSD_TB_ABBREVIATION')
# MSD_TB_ALIAS_PANEL = os.environ.get('MSD_TB_ALIAS_PANEL', 'MSD_TB_ALIAS_PANEL')
# MSD_TB_ASSEMBLY_SET = os.environ.get('MSD_TB_ASSEMBLY_SET', 'MSD_TB_ASSEMBLY_SET')
# MSD_TB_GROUPING = os.environ.get('MSD_TB_GROUPING', 'MSD_TB_GROUPING')
# MSD_TB_HARGA = os.environ.get('MSD_TB_HARGA', 'MSD_TB_HARGA')
M_SPART_IMAGE = os.environ.get('M_SPART_IMAGE', 'M_SPART_IMAGE')
M_LINK_IMG = os.environ.get('M_LINK_IMG', 'M_LINK_IMG')
# MSD_TB_MEREK_KEND = os.environ.get('MSD_TB_MEREK_KEND', 'MSD_TB_MEREK_KEND')
# MSD_TB_MODEL_COVERED = os.environ.get('MSD_TB_MODEL_COVERED', 'MSD_TB_MODEL_COVERED')
# MSD_TB_MODEL_KEND = os.environ.get('MSD_TB_MODEL_KEND', 'MSD_TB_MODEL_KEND')
# MSD_TB_PANEL_MASTER = os.environ.get('MSD_TB_PANEL_MASTER', 'MSD_TB_PANEL_MASTER')
# MSD_TB_SPAREPART = os.environ.get('MSD_TB_SPAREPART', 'MSD_TB_SPAREPART')
# MSD_TB_MASTER_KEND = os.environ.get('MSD_TB_MASTER_KEND', 'MSD_TB_MASTER_KEND')
# TB_PANEL_MATCHING_TEST2 = os.environ.get('TB_PANEL_MATCHING_TEST2', 'TB_PANEL_MATCHING_TEST2')
# MSD_TB_MAPPING_MST_KEND = os.environ.get('MSD_TB_MAPPING_MST_KEND', 'MSD_TB_MAPPING_MST_KEND')


class MSparepartVin(Base):
    __tablename__ = m_sparepart_vin

    NOU = Column(NUMBER(10), primary_key=True)
    NO_RANGKA = Column(VARCHAR2(20))
    KATEGORI_PART = Column(VARCHAR2(50))
    BAGIAN_PART = Column(VARCHAR2(70))
    NO_PART = Column(VARCHAR2(30))
    NAMA_PART = Column(VARCHAR2(70))
    NAMA_PANEL = Column(VARCHAR2(70))
    SISI_PANEL = Column(VARCHAR2(20))
    CODE = Column(VARCHAR2(100))
    NOTE = Column(VARCHAR2(1000))
    QTY_REQUIRED = Column(NUMBER(3))
    PROD_DATE = Column(VARCHAR2(50))
    MODEL = Column(VARCHAR2(100))
    TRANSMISION = Column(VARCHAR2(10))
    NO_RANGKA_10D = Column(VARCHAR2(10))
    TIPE = Column(VARCHAR2(50))
    LDR_ID = Column(VARCHAR2(5))
    LKB_ID = Column(VARCHAR2(1))
    REF_ASSEMBLY = Column(VARCHAR2(25))
    REP_PART = Column(VARCHAR2(25))
    QTY_REP_PART = Column(VARCHAR2(3))
    SUMBER = Column(VARCHAR2(20))
    ID_LAMA = Column(VARCHAR2(25))
    ID_MODEL_COVERED = Column(VARCHAR2(10))

class MsdTbImageSparepart(Base):
    __tablename__ = M_SPART_IMAGE

    ID_IMAGE = Column(VARCHAR2(255), primary_key=True)
    IMAGE_NAME = Column(VARCHAR2(100))
    SECTION_IMAGE = Column(VARCHAR2(5))
    IMAGE = Column(CLOB)


class MsdTbLinkImageSparepart(Base):
    __tablename__ = M_LINK_IMG

    ID_LINK_IMAGE = Column(NUMBER, primary_key=True)
    ID_IMAGE = Column(VARCHAR2(40))
    ID_SPAREPART = Column(VARCHAR2(40))


# class MsdTbVin(Base):
#     __tablename__ = MSD_TB_VIN

#     id_vin = Column(VARCHAR2(20), primary_key=True)
#     vin = Column(VARCHAR2(20))
#     id_model_covered = Column(VARCHAR2(9))
#     grade = Column(VARCHAR2(20))
#     transmission = Column(VARCHAR2(10))
#     displacement = Column(VARCHAR2(30))
#     engine = Column(VARCHAR2(30))
#     wheel_drive = Column(VARCHAR2(30))
#     drive = Column(VARCHAR2(10))
#     body_kend = Column(VARCHAR2(30))
#     seating_number = Column(VARCHAR2(10))
#     door_number = Column(VARCHAR2(10))
#     area = Column(VARCHAR2(10))
#     prod_from = Column(NUMBER(precision=5, asdecimal=False))
#     prod_upto = Column(NUMBER(precision=5, asdecimal=False))


# class MsdTbAliasPanel(Base):
#     __tablename__ = MSD_TB_ALIAS_PANEL

#     id_alias_sparepartmsd = Column(NUMBER, primary_key=True)
#     id_merek_kend = Column(VARCHAR2(8))
#     id_sparepart = Column(VARCHAR2(23))
#     id_panel = Column(VARCHAR2(8))


# class MsdTbAssemblySet(Base):
#     __tablename__ = MSD_TB_ASSEMBLY_SET

#     id_assembly_set = Column(VARCHAR2(6), primary_key=True)
#     assembly_set = Column(VARCHAR2(300))
#     ref_assembly_set = Column(VARCHAR2(10))
#     batch = Column(VARCHAR2(5))


# class MsdTbGrouping(Base):
#     __tablename__ = MSD_TB_GROUPING

#     id_group_part = Column(VARCHAR2(5), primary_key=True)
#     group_part = Column(VARCHAR2(50))
#     batch = Column(VARCHAR2(5))


# class MsdTbHarga(Base):
#     __tablename__ = MSD_TB_HARGA

#     id_harga = Column(NUMBER, primary_key=True)
#     id_sparepart = Column(VARCHAR2(23))
#     currency = Column(VARCHAR2(3))
#     harga = Column(NUMBER(14, 2))
#     last_update = Column(TIMESTAMP)
#     sumber = Column(VARCHAR2(20))
#     job_id = Column(VARCHAR2(32))


# class MsdTbImageSparepart(Base):
#     __tablename__ = MSD_TB_IMAGE_SPAREPART

#     id_image = Column(VARCHAR2(255), primary_key=True)
#     file_image = Column(BLOB)
#     image_name = Column(VARCHAR2(100))
#     section_image = Column(VARCHAR2(5))


# class MsdTbLinkImageSparepart(Base):
#     __tablename__ = MSD_TB_LINK_IMAGE_SPAREPART

#     id_link_image = Column(NUMBER, primary_key=True)
#     id_sparepart = Column(VARCHAR2(127))
#     id_image = Column(VARCHAR2(127))


# class MsdTbMerekKend(Base):
#     __tablename__ = MSD_TB_MEREK_KEND

#     id_merek_kend = Column(VARCHAR2(8), primary_key=True)
#     merek_kend = Column(VARCHAR2(20))


# class MsdTbModelCovered(Base):
#     __tablename__ = MSD_TB_MODEL_COVERED

#     id_model_covered = Column(VARCHAR2(9), primary_key=True)
#     id_model_kend = Column(VARCHAR2(6))
#     grade = Column(VARCHAR2(20))
#     transmission = Column(VARCHAR2(10))
#     displacement = Column(VARCHAR2(30))
#     engine = Column(VARCHAR2(30))
#     wheel_drive = Column(VARCHAR2(30))
#     drive = Column(VARCHAR2(20))
#     body_kend = Column(VARCHAR2(30))
#     seating_number = Column(VARCHAR2(20))
#     door_number = Column(VARCHAR2(20))
#     area = Column(VARCHAR2(20))
#     prod_from = Column(NUMBER(precision=5, asdecimal=False))
#     prod_upto = Column(NUMBER(precision=5, asdecimal=False))
#     batch = Column(VARCHAR2(5))


# class MsdTbModelKend(Base):
#     __tablename__ = MSD_TB_MODEL_KEND

#     id_model_kend = Column(VARCHAR2(6), primary_key=True)
#     id_merek_kend = Column(VARCHAR2(8))
#     model_kend = Column(VARCHAR2(30))
#     kode_model_kend = Column(VARCHAR2(30))


# class MsdTbPanelMaster(Base):
#     __tablename__ = MSD_TB_PANEL_MASTER

#     id_panel = Column(VARCHAR2(8), primary_key=True)
#     nama_panel = Column(VARCHAR2(100))


# class MsdTbSparepart(Base):
#     __tablename__ = MSD_TB_SPAREPART

#     id_sparepart = Column(VARCHAR2(23), primary_key=True)
#     id_model_covered = Column(VARCHAR2(9))
#     id_group_part = Column(VARCHAR2(5))
#     id_assembly_set = Column(VARCHAR2(6))
#     ref_no = Column(VARCHAR2(15))
#     part_number = Column(VARCHAR2(50))
#     part_name = Column(VARCHAR2(255))
#     qty = Column(VARCHAR2(20))
#     rep_part = Column(VARCHAR2(50))
#     qty_rep_part = Column(VARCHAR2(10))
#     deskripsi = Column(VARCHAR2(300))
#     sumber = Column(VARCHAR2(255))
#     batch = Column(VARCHAR2(5))
#     app_from = Column(NUMBER(precision=4, asdecimal=False))
#     app_upto = Column(NUMBER(precision=4, asdecimal=False))
#     remark_rep_part = Column(VARCHAR2(1))


# class JobMixin(object):
#     job_id = Column('job_id', VARCHAR2(32), primary_key=True)


# class SparepartIsuzu(JobMixin, Base):
#     __tablename__ = "scraping_sparepart_isuzu"

#     id = Column(Integer, primary_key=True)
#     merk = Column('merk', VARCHAR2(50))
#     model_mobil = Column('model_mobil', VARCHAR2(50))
#     tipe_mobil = Column('tipe_mobil', VARCHAR2(50))
#     main_group = Column('main_group', VARCHAR2(100))
#     assembly_set = Column('assembly_set', VARCHAR2(255))
#     key = Column('key_', VARCHAR2(10))
#     part_number = Column('part_number', VARCHAR2(255))
#     itc = Column('itc', VARCHAR2(10))
#     description = Column('description', VARCHAR2(255))
#     qty = Column('qty', VARCHAR2(10))
#     app_date = Column('app_date', VARCHAR2(10))
#     lr = Column('lr', VARCHAR2(10))
#     model = Column('model', VARCHAR2(100))
#     remarks = Column('remarks', VARCHAR2(255))
#     source_url = Column('source_url', VARCHAR2(255))


# class SparepartParts(JobMixin, Base):
#     __tablename__ = "scraping_sparepart_parts"

#     id = Column(Integer, primary_key=True)
#     source_url = Column('source_url', VARCHAR2(255))
#     merk = Column('merk', VARCHAR2(50))
#     model_year = Column('model_year', VARCHAR2(25))
#     model_mobil = Column('model_mobil', VARCHAR2(50))
#     submodel = Column('submodel', VARCHAR2(50))
#     engine = Column('engine', VARCHAR2(50))
#     section = Column('section', VARCHAR2(100))
#     group = Column('group', VARCHAR2(100))
#     subgroup = Column('subgroup', VARCHAR2(100))
#     part_name = Column('part_name', VARCHAR2(255))
#     part_number = Column('part_number', VARCHAR2(255))
#     price = Column('price', VARCHAR2(100))
#     description = Column('description', VARCHAR2(255))
#     lookup_no = Column('lookup_no', VARCHAR2(50))
#     image_id = Column(Integer, nullable=True)


# class SparepartMegazip(JobMixin, Base):
#     __tablename__ = "scraping_sparepart_megazip"

#     id = Column(Integer, primary_key=True)
#     image_id = Column(Integer, nullable=True)
#     source_url = Column('source_url', VARCHAR2(255))
#     merk = Column('merk', VARCHAR2(50))
#     varian = Column('varian', VARCHAR2(25))
#     model = Column('model', VARCHAR2(50))
#     vehicle_model = Column('vehicle_model', VARCHAR2(50))
#     model_mark = Column('model_mark', VARCHAR2(50))
#     model_year = Column('model_year', VARCHAR2(25))
#     frame = Column('frame', VARCHAR2(50))
#     grade = Column('grade', VARCHAR2(50))
#     body = Column('body', VARCHAR2(50))
#     engine = Column('engine', VARCHAR2(50))
#     transmission = Column('transmission', VARCHAR2(50))
#     destination = Column('destination', VARCHAR2(50))
#     from_date = Column('from_date', VARCHAR2(10))
#     to_date = Column('to_date', VARCHAR2(10))
#     gear_shift_type = Column('gear_shift_type', VARCHAR2(50))
#     transmission = Column('transmission', VARCHAR2(50))
#     seating_capacity = Column('seating_capacity', VARCHAR2(50))
#     fuel_induction = Column('fuel_induction', VARCHAR2(50))
#     drive = Column('drive', VARCHAR2(50))
#     door_number = Column('door_number', VARCHAR2(50))
#     note = Column('note', VARCHAR2(50))
#     assembly_group = Column('assembly_group', VARCHAR2(255))
#     assembly_set = Column('assembly_set', VARCHAR2(255))
#     reference = Column('reference', VARCHAR2(25))
#     part_name = Column('part_name', VARCHAR2(255))
#     part_number = Column('part_number', VARCHAR2(255))
#     replacement_for = Column('replacement_for', VARCHAR2(255))
#     price = Column('price', Text())
#     description = Column('description', VARCHAR2(255))


# class SparepartSuzuki(JobMixin, Base):
#     __tablename__ = "scraping_sparepart_suzuki"

#     id = Column(Integer, primary_key=True, autoincrement=False)
#     image_id = Column(Integer, nullable=True)
#     source_url = Column('source_url', VARCHAR2(255))
#     merk = Column('merk', VARCHAR2(50))
#     model = Column('model', VARCHAR2(50))
#     group = Column('group', VARCHAR2(50))
#     assembly_set = Column('assembly_set', VARCHAR2(255))
#     part_name = Column('part_name', VARCHAR2(255))
#     part_number = Column('part_number', VARCHAR2(255))
#     substitution_part_number = Column('substitution_part_number', VARCHAR2(100))
#     qty = Column('qty', VARCHAR2(10))
#     price = Column('price', VARCHAR2(255))
#     remarks = Column('remarks', VARCHAR2(255))
#     tag_no = Column('tag_no', VARCHAR2(255))


# class SparepartDaihatsu(JobMixin, Base):
#     __tablename__ = "scraping_sparepart_daihatsu"

#     id = Column(Integer, primary_key=True)
#     image_id = Column(Integer, nullable=True)
#     source_url = Column('source_url', VARCHAR2(255))
#     merk = Column('merk', VARCHAR2(50))
#     model = Column('model', VARCHAR2(50))
#     group = Column('group', VARCHAR2(50))
#     assembly_set = Column('assembly_set', VARCHAR2(255))
#     prod_date = Column('prod_date', VARCHAR2(100))
#     part_name = Column('part_name', VARCHAR2(255))
#     part_number = Column('part_number', VARCHAR2(255))
#     price = Column('price', VARCHAR2(255))


# class ScrapingJob(Base):
#     __tablename__ = 'scraping_job'

#     id = Column(VARCHAR2(32), primary_key=True)
#     spider = Column('spider', VARCHAR2(50))
#     input_param = Column('input_param', VARCHAR2(1000))
#     status = Column('status', VARCHAR2(25))
#     reason = Column('reason', VARCHAR2(25))
#     start = Column('start', TIMESTAMP, nullable=True)
#     finish = Column('finish', TIMESTAMP, nullable=True)
#     log = Column('log', Text(length=1073741824), nullable=True)
#     jobdir = Column('jobdir', VARCHAR2(100), nullable=True)


# class TbPanelMatchingTest2(Base):
#     __tablename__="TB_PANEL_MATCHING_TEST2"

#     ID_MATCHING = Column(NUMBER(38,0), primary_key=True)
#     nama_panel = Column('nama_panel', VARCHAR2(100))
#     indeks_lokasi = Column('indeks_lokasi', VARCHAR2(4))
#     derek = Column('derek', NUMBER(38,0))
#     pasal_352 = Column('pasal_352', NUMBER(38,0))
#     id_panel = Column('id_panel', VARCHAR2(8))



# class MsdTbAbbreviation(Base):
#     __tablename__ = MSD_TB_ABBREVIATION

#     id_abbreviation = Column(NUMBER, primary_key=True)
#     id_merek_kend = Column(VARCHAR2(8))
#     mark = Column(VARCHAR2(50))
#     definition = Column(VARCHAR2(255))
#     sumber = Column(VARCHAR2(255))

# class MsdTbMasterKend(Base):
#     __tablename__ = MSD_TB_MASTER_KEND

#     id_master_kend = Column(VARCHAR2(10), primary_key=True)
#     id_merek_kend = Column(VARCHAR2(20))
#     kode_tipe_kend = Column(VARCHAR2(8))
#     merk_kendaraan = Column(VARCHAR2(100))
#     tipe_kendaraan = Column(VARCHAR2(255))
#     jenis_kendaraan = Column(VARCHAR2(100))
#     tahun_rakit = Column(NUMBER(precision=5, asdecimal=False))


# class MsdTbMappingMstKend(Base):
#     __tablename__ = MSD_TB_MAPPING_MST_KEND

#     no_kend_covered = Column(NUMBER, primary_key=True)
#     id_model_covered = Column(VARCHAR2(9))
#     id_master_kend = Column(VARCHAR2(10))