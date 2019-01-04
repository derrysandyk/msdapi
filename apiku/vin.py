import falcon
import json
from sqlalchemy import and_, or_, between, func
from sqlalchemy.orm import aliased
from sqlalchemy.dialects import oracle
from .base import BaseResource
from .falcon_pagination.offset_pagination_hook import OffsetPaginationHook
from .database import session_scope
from .inis import MsdTbAliasPanel, MsdTbAssemblySet, MsdTbGrouping, MsdTbHarga, MsdTbImageSparepart\
    , MsdTbLinkImageSparepart, MsdTbMerekKend, MsdTbModelCovered, MsdTbModelKend, MsdTbPanelMaster, MsdTbSparepart\
    , MsdTbVin, TbPanelMatchingTest2
# from .sparepart_search import get_harga_by_sparepart
from .utils import alchemyencoder
# from .sparepart_search import get_sumber_from_sparepart, get_image_ids
import math
from functools import lru_cache
from .rediscache import my_cache,cache_it_json, cache_it
from .sparepart_search import get_abbreviation

class Resource3(BaseResource):
    @falcon.before(OffsetPaginationHook(
    default_limit=10,
    max_limit=500,
    offset_key='offset',
    limit_key='limit'))
    def on_get(self, req, resp):
        # session = session_scope()
        with self.session_scope() as session:
                # imageselected = image.__table__.columns
            params = req.params
            print('req.params', req.params)
            id_panel = params.get('id_panel', None)
            id_model_covered = params.get('id_model_covered', None)
            part_number = params.get('part_number', None)
            if id_panel == 'None':
                id_panel = None

            if not id_model_covered or not part_number:
                resp.body = json.dumps({'message': 'one of query parameter is empty'})
                resp.status = falcon.HTTP_400
                return

            

            all_query_params = {}

            if id_panel:
                all_query_params['id_panel'] = id_panel
            if id_model_covered:
                all_query_params['id_model_covered'] = id_model_covered
            if part_number:
                all_query_params['part_number'] = part_number

            def query_builder(id_panel=None, id_model_covered=None, part_number=None, sumber=None):
                
                sp = aliased(MsdTbSparepart)
                ap = aliased(MsdTbAliasPanel)
                pl = aliased(MsdTbPanelMaster)
                mc = aliased(MsdTbModelCovered)
                merek = aliased(MsdTbMerekKend)
                mdl = aliased(MsdTbModelKend)
                asse = aliased(MsdTbAssemblySet)
                gr = aliased(MsdTbGrouping)
                pm1 = aliased(TbPanelMatchingTest2)
                pm2 = aliased(TbPanelMatchingTest2)
                th = aliased(MsdTbHarga)
                th_ = aliased(MsdTbHarga)
                indeks_lokasi_query = session.query(pm2.indeks_lokasi).distinct()\
                    .filter(and_(pm2.id_panel == id_panel))\
                    .subquery()
                id_panel_query = session.query(pm1.id_panel).distinct()\
                    .filter(pm1.indeks_lokasi.in_(indeks_lokasi_query))\
                    .subquery()
                harga_query = session.query(th.id_sparepart, func.max(th.last_update).label("latest")) \
                    .filter(th.id_sparepart == sp.id_sparepart) \
                    .group_by(th.id_sparepart) \
                    .subquery()

                co_occurrence_panel_matching_fields = (
                    sp.id_sparepart, sp.part_name, sp.part_number
                      , th_.currency, th_.harga
                      , pl.nama_panel, asse.assembly_set
                      , gr.group_part, merek.merek_kend, mdl.model_kend, mc.prod_from, mc.prod_upto, mc.displacement
                      , mc.transmission, sp.ref_no, sp.qty, sp.rep_part, sp.qty_rep_part, sp.deskripsi, sp.app_from
                      , sp.app_upto, sp.remark_rep_part, mc.grade, mc.wheel_drive, mc.drive, mc.body_kend
                      , mc.seating_number, mc.door_number, mc.area
                      , pl.id_panel, mc.id_model_covered, merek.id_merek_kend
                )
                co_occurrence_panel_matching_query = session.query(*co_occurrence_panel_matching_fields).select_from(ap).distinct()\
                    .join(pl, pl.id_panel == ap.id_panel)\
                    .join(sp, sp.id_sparepart == ap.id_sparepart)\
                    .join(mc, mc.id_model_covered == sp.id_model_covered)\
                    .join(mdl, mdl.id_model_kend == mc.id_model_kend)\
                    .join(merek, merek.id_merek_kend == mdl.id_merek_kend)\
                    .join(asse, asse.id_assembly_set == sp.id_assembly_set)\
                    .join(gr, gr.id_group_part == sp.id_group_part)\
                    .outerjoin(harga_query, harga_query.c.id_sparepart == sp.id_sparepart)\
                    .outerjoin(th_, and_(th_.last_update == harga_query.c.latest, th_.id_sparepart == sp.id_sparepart))\
                    .filter(pl.id_panel.in_(id_panel_query))\
                    .filter(mc.id_model_covered == id_model_covered)\
                    .filter(sp.part_number != part_number)
            
                sp2 = aliased(MsdTbSparepart)
                ap2 = aliased(MsdTbAliasPanel)
                pl2 = aliased(MsdTbPanelMaster)
                mc2 = aliased(MsdTbModelCovered)
                merek2 = aliased(MsdTbMerekKend)
                mdl2 = aliased(MsdTbModelKend)
                asse2 = aliased(MsdTbAssemblySet)
                gr2 = aliased(MsdTbGrouping)
                th2 = aliased(MsdTbHarga)

                harga_query_for_assembly = session.query(th2.id_sparepart, func.max(th2.last_update).label("latest")) \
                    .filter(th2.id_sparepart == sp2.id_sparepart) \
                    .group_by(th2.id_sparepart) \
                    .subquery()
                co_occurrence_from_assembly_fields = (
                    sp.id_sparepart, sp.part_name, sp.part_number
                      , th_.currency, th_.harga
                      , pl.nama_panel, asse.assembly_set
                      , gr.group_part, merek.merek_kend, mdl.model_kend, mc.prod_from, mc.prod_upto, mc.displacement
                      , mc.transmission, sp.ref_no, sp.qty, sp.rep_part, sp.qty_rep_part, sp.deskripsi, sp.app_from
                      , sp.app_upto, sp.remark_rep_part, mc.grade, mc.wheel_drive, mc.drive, mc.body_kend
                      , mc.seating_number, mc.door_number, mc.area
                      , pl.id_panel, mc.id_model_covered, merek2.id_merek_kend
                )
                id_assembly_set = session.query(MsdTbSparepart.id_assembly_set)\
                    .filter(MsdTbSparepart.id_model_covered == id_model_covered)\
                    .filter(MsdTbSparepart.part_number == part_number).first()[0]
                co_occurrence_from_assembly_query = session.query(*co_occurrence_from_assembly_fields).select_from(sp2).distinct()\
                    .outerjoin(ap2, ap2.id_sparepart == sp2.id_sparepart)\
                    .outerjoin(pl2, pl2.id_panel == ap2.id_panel)\
                    .join(mc2, mc2.id_model_covered == sp2.id_model_covered)\
                    .join(mdl2, mdl2.id_model_kend == mc2.id_model_kend)\
                    .join(merek2, merek2.id_merek_kend == mdl2.id_merek_kend)\
                    .join(asse2, asse2.id_assembly_set == sp2.id_assembly_set)\
                    .join(gr2, gr2.id_group_part == sp2.id_group_part)\
                    .join(harga_query_for_assembly, harga_query_for_assembly.c.id_sparepart == sp2.id_sparepart)\
                    .join(th_, and_(th_.last_update == harga_query_for_assembly.c.latest, th_.id_sparepart == sp2.id_sparepart))\
                    .filter(mc2.id_model_covered == id_model_covered)\
                    .filter(asse2.id_assembly_set == id_assembly_set)\
                    .filter(sp2.part_number != part_number)
                all_query = ""
                if sumber:
                    if id_panel:
                        all_query = co_occurrence_panel_matching_query.filter(sp.sumber.ilike('%{}%'.format(sumber)))\
                        .union(co_occurrence_from_assembly_query.filter(sp2.sumber.ilike('%{}%'.format(sumber))))
                    else:
                        all_query = co_occurrence_from_assembly_query.filter(sp2.sumber.ilike('%{}%'.format(sumber)))
                else:
                    if id_panel:
                        all_query = co_occurrence_panel_matching_query.union(co_occurrence_from_assembly_query)
                    else:
                        all_query = co_occurrence_from_assembly_query

                # print(all_query)
                return all_query

            @cache_it(cache=my_cache, expire=60*10)
            def run_query_total_count(**kwargs):
                return query_builder(**kwargs).count()

            @cache_it(cache=my_cache, expire=60*10)
            def run_query_current_count(limit, offset, **kwargs):
                return query_builder(**kwargs).limit(limit).offset(offset).count()

            @cache_it(cache=my_cache, expire=60*10)
            def run_query(limit, offset, **kwargs):
                result = query_builder(**kwargs).limit(limit).offset(offset)
                retval = []
                for row_itm in result:
                    retval.append(row_itm)
                return retval

            try:
                page = int(params.get('page', 1))
                limit = int(req.context['pagination']['limit'])
                # get sumbers
                sumbers = get_sumber_from_sparepart()
                total_data = []
                # response object dictionary
                
                # resp_obj = {}
                # for index, value in enumerate(co_occurrence_panel_matching_fields):
                #     resp_obj[value.key] = None

                # print('resp_obj.............', resp_obj)
                # resp.status = falcon.HTTP_200
                # return

                # total_count = total_row_count = 0
            
                objects = {}
                total_count = 0
                for sumber in sumbers:

                    all_query_params.update({'sumber': sumber})
                    total_count_sumber = run_query_total_count(**all_query_params)
                    if total_count_sumber == 0:
                        continue

                    total_count += total_count_sumber

                    offset = (page - 1) * limit
                    current_count = run_query_current_count(limit, offset, **all_query_params)
                    total_data.append(current_count)
                    
                    # test_query = all_query.limit(limit).offset((page - 1) * limit)
                    data_from_sumber = run_query(limit, offset, **all_query_params)
                    for row in data_from_sumber:
                        # 
                        data = {}

                        fields = ('id_sparepart', 'part_name', 'part_number'
                                , 'currency', 'harga'
                                , 'nama_panel', 'assembly_set'
                                , 'group_part', 'merek_kend', 'model_kend', 'prod_from', 'prod_upto', 'displacement'
                                , 'transmission', 'ref_no', 'qty', 'rep_part', 'qty_rep_part', 'deskripsi', 'app_from'
                                , 'app_upto', 'remark_rep_part', 'grade', 'wheel_drive', 'drive', 'body_kend'
                                , 'seating_number', 'door_number', 'area'
                                , 'id_panel', 'id_model_covered' , 'id_merek_kend'
                                # , 'vin'
                                )
                        # data = {}
                        for index, value in enumerate(fields):
                            data[value] = row[index]

                        # get id_image
                        sparepart_id = row[0]
                        id_merek_kend = row[-1]
                        data['image'] = get_image_ids(sparepart_id)
                        data['abbreviation'] = get_abbreviation(id_merek_kend)

                        if sumber not in objects:
                            objects[sumber] = []

                        objects[sumber].append(data)
                        

                total_page = math.ceil(total_count / limit)
                main_params = "/co_occurrence/?id_panel={0}&id_model_covered={1}&part_number={2}&limit={3}".format(
                    id_panel, id_model_covered, part_number, limit)

                if page == 1:
                    prev_page = None
                else:
                    the_page = min(total_page, page - 1)
                    prev_page = "{0}&page={1}".format(main_params, the_page)

                if total_page <= page:
                    nex_page = None
                else:
                    nex_page = "{0}&page={1}".format(main_params, page + 1)

                respon = {
                    "count": total_count,
                    "next": nex_page,
                    "previous": prev_page,
                    "results": objects
                }
                resp.body = json.dumps(respon, default=alchemyencoder)
                resp.status = falcon.HTTP_200

                # print('--------------------------------QUERY', all_query, id_assembly_set)

            except Exception as e:

                resp.body = json.dumps({'error': '{} - {}'.format(type(e), str(e))})
                resp.status = falcon.HTTP_500

@cache_it(cache=my_cache)
def get_image_ids(id_sparepart=None):
    result = []
    if not id_sparepart:
        return result

    with session_scope() as session:
        sp = aliased(MsdTbSparepart)
        li = aliased(MsdTbLinkImageSparepart)
        isp = aliased(MsdTbImageSparepart)
        image = session.query(isp.id_image) \
            .join(li, isp.id_image == li.id_image) \
            .join(sp, sp.id_sparepart == li.id_sparepart) \
            .filter(sp.id_sparepart == id_sparepart)
        for res in image.all():
            link_image = "/image/?id_image={0}".format(res[0])
            result.append(link_image)
        session.close()
        return result

@cache_it(cache=my_cache, expire=60*60*24*7)
def get_sumber_from_sparepart():
    with session_scope() as session:
        sumbers = [itm[0] for itm in session.query(MsdTbSparepart.sumber).distinct()]
        sumbers.sort()
        session.close()
        return sumbers
            # params = req.params
            # print('req.params', req.params)
            # id_panel = params.get('id_panel', None)
            # id_model_covered = params.get('id_model_covered', None)
            # part_number = params.get('part_number', None)
            # if not id_panel or not id_model_covered or not part_number:
            #     resp.status = falcon.HTTP_400
            #     return

            # # session = Session()
            # sp = aliased(MsdTbSparepart)
            # ap = aliased(MsdTbAliasPanel)
            # pl = aliased(MsdTbPanelMaster)
            # mc = aliased(MsdTbModelCovered)
            # merek = aliased(MsdTbMerekKend)
            # mdl = aliased(MsdTbModelKend)
            # asse = aliased(MsdTbAssemblySet)
            # gr = aliased(MsdTbGrouping)
            # pm1 = aliased(TbPanelMatchingTest2)
            # pm2 = aliased(TbPanelMatchingTest2)

            # indeks_lokasi_query = session.query(pm2.indeks_lokasi).distinct()\
            #     .filter(pm2.id_panel == id_panel)\
            #     .subquery()
            # id_panel_query = session.query(pm1.id_panel).distinct()\
            #     .filter(pm1.indeks_lokasi.in_(indeks_lokasi_query))\
            #     .subquery()

            # co_occurrence_fields = (
            #     sp.id_sparepart, sp.part_name, sp.part_number, pl.nama_panel, ap.id_panel, asse.assembly_set
            #     , gr.group_part, merek.merek_kend, mdl.model_kend, mc.prod_from, mc.prod_upto, mc.displacement
            #     , mc.transmission, sp.ref_no, sp.qty, sp.rep_part, sp.qty_rep_part, sp.deskripsi, sp.app_from
            #     , sp.app_upto, sp.remark_rep_part, mc.grade, mc.wheel_drive, mc.drive, mc.body_kend
            #     , mc.seating_number, mc.door_number, mc.area, pl.id_panel
            # )
            # co_occurrence_query = session.query(*co_occurrence_fields).select_from(ap).distinct()\
            #     .join(pl, pl.id_panel == ap.id_panel)\
            #     .join(sp, sp.id_sparepart == ap.id_sparepart)\
            #     .join(mc, mc.id_model_covered == sp.id_model_covered)\
            #     .join(mdl, mdl.id_model_kend == mc.id_model_kend)\
            #     .join(merek, merek.id_merek_kend == mdl.id_merek_kend)\
            #     .join(asse, asse.id_assembly_set == sp.id_assembly_set)\
            #     .join(gr, gr.id_group_part == sp.id_group_part)\
            #     .filter(pl.id_panel.in_(id_panel_query))\
            #     .filter(mc.id_model_covered == id_model_covered)\
            #     .filter(sp.part_number != part_number)\
            #     .order_by(sp.id_sparepart)

            # print('co_occurrence_query', co_occurrence_query)

            # objects_list = []
            # for row in co_occurrence_query:
            #     data = {}
            #     for index, value in enumerate(co_occurrence_fields):
            #         data[value.key] = row[index]
            #     objects_list.append(data)

            # resp.body = json.dumps(objects_list, default=alchemyencoder)
            # resp.status = falcon.HTTP_200

# @lru_cache(maxsize=128)
# def get_harga_by_sparepart(id_sparepart=None):
#     if not id_sparepart:
#         return {}

#     with session_scope() as session:
#         try:
#             fields = (MsdTbHarga.currency, MsdTbHarga.harga, MsdTbHarga.last_update)
#             harga = session.query(*fields) \
#                 .filter(MsdTbHarga.id_sparepart == id_sparepart).order_by(MsdTbHarga.last_update.desc()).first()
#             data = {}
#             for index, value in enumerate(fields):
#                 data[value.key] = getattr(harga, value.key)
#             return data
#         except Exception as e:
#             return {}

# import json
# import falcon
# import cx_Oracle
# import collections
# from sqlalchemy.orm import aliased
# from .auth import AuthMiddleware as am
# from .inis import MsdTbAliasPanel, MsdTbPanelMaster, MsdTbSparepart\
#     , MsdTbVin , MsdTbModelCovered , MsdTbHarga, TbPanelMatchingTest2
# from sqlalchemy import func
# from .utils import alchemyencoder
# from .base import BaseResource
# class Resource3(BaseResource):
#     # @falcon.before(am.validate_auth)
#     def on_get(self, req, resp):
#         with self.session_scope() as session:
#             params = req.params
#             vin_code = params.get('vin', None)
#             panel = params.get('nama_panel', None)

#             sp = aliased(MsdTbSparepart)
#             vin_tb = aliased(MsdTbVin)
#             ap = aliased(MsdTbAliasPanel)
#             pl = aliased(MsdTbPanelMaster)
#             mc = aliased(MsdTbModelCovered)
#             th = aliased(MsdTbHarga)
#             pm = aliased(TbPanelMatchingTest2)

#             fields = (sp.id_sparepart, sp.part_name, sp.part_number, th.currency, th.harga, pl.nama_panel, ap.id_panel
#                     )
#             vin = session.query(*fields).select_from(vin_tb).distinct()\
#                 .join(mc, vin_tb.id_model_covered == mc.id_model_covered) \
#                 .join(sp, sp.id_model_covered == mc.id_model_covered) \
#                 .outerjoin(th, sp.id_sparepart == th.id_sparepart)\
#                 .join(ap, sp.id_sparepart == ap.id_sparepart)\
#                 .join(pl, ap.id_panel == pl.id_panel)\
#                 .filter(func.lower(vin_tb.vin) == func.lower(vin_code)) \
#                 .filter(pl.nama_panel.ilike('%{}%'.format(panel)))\
#                 .order_by(sp.id_sparepart)
#             # print(vin)
#             panel_list = set()
#             objects_data_vin = []
#             for row in vin:
#                 data = {}
#                 for index, value in enumerate(fields):
#                     data[value.key] = row[index]
#                 panel_list.add(row[6])
#                 objects_data_vin.append(data)
#                 break

#             panel_master = session.query(pm.indeks_lokasi).select_from(pl).distinct()\
#                 .join(pm, pm.id_panel == pl.id_panel)\
#                 .filter(pl.nama_panel.ilike('%{}%'.format(panel)))

#             index_lokasi = set()
#             for row in panel_master:
#                 index_lokasi.add(row[0])
#             print(index_lokasi)

#             panel_match = session.query(pm.id_panel).select_from(pm).distinct()\
#                 .filter(pm.indeks_lokasi.in_(index_lokasi))

#             id_panel= []
#             for row in panel_match:
#                 # for index, value in enumerate(fields):
#                 id_panel.append(row[0])
#             print(id_panel)
#             print(panel_list)
#             fields2 = (sp.id_sparepart, sp.part_name, sp.part_number, th.currency, th.harga, pl.nama_panel, ap.id_panel
#                     )
#             coocurence = session.query(*fields2).select_from(vin_tb).distinct() \
#                 .join(mc, vin_tb.id_model_covered == mc.id_model_covered) \
#                 .join(sp, sp.id_model_covered == mc.id_model_covered) \
#                 .outerjoin(th, sp.id_sparepart == th.id_sparepart) \
#                 .join(ap, sp.id_sparepart == ap.id_sparepart) \
#                 .join(pl, ap.id_panel == pl.id_panel) \
#                 .filter(func.lower(vin_tb.vin) == func.lower(vin_code)) \
#                 .filter(~ap.id_panel.in_(panel_list))\
#                 .filter(ap.id_panel.in_(id_panel))\
#                 .order_by(sp.id_sparepart)


#             objects_data_coocurence = []
#             for row in coocurence:
#                 data = {}
#                 for index, value in enumerate(fields):
#                     data[value.key] = row[index]
#                 objects_data_coocurence.append(data)
#             temp = {
#                 'panel_info': objects_data_vin,
#                 'co_occurrence': objects_data_coocurence
#             }
#             resp.body = json.dumps(temp, default=alchemyencoder)
#             resp.status = falcon.HTTP_200