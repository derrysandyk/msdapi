import falcon
import json
from sqlalchemy import and_, or_, between, func, desc
from sqlalchemy.orm import aliased
# from datetime import datetime
import cx_Oracle
from sqlalchemy.dialects import oracle
from .base import BaseResource
from sqlalchemy.sql.functions import coalesce
from .falcon_pagination.offset_pagination_hook import OffsetPaginationHook
from .database import session_scope
from .inis import MSparepartVin,MsdTbLinkImageSparepart
from .utils import alchemyencoder
import math
from .rediscache import my_cache,cache_it_json, cache_it
# from rediscache import cache_it_json, cache_it
from .auth import AuthMiddleware
class sparepart_search(BaseResource):
    @falcon.before(OffsetPaginationHook(
    default_limit=10,
    max_limit=100,
    offset_key='offset',
    limit_key='limit'))
    # @falcon.before(AuthMiddleware.validate_auth)
    def on_get(self, req, resp):
        # session = session_scope()
        with self.session_scope() as session:
            params = req.params

            no_rangka = req.get_param("no_rangka")
            nama_panel = req.get_param("nama_panel")
            sisi_panel = req.get_param("sisi_panel")
            # print(params)
            list_params = []
            valid_params = ('no_rangka', 'nama_panel', 'sisi_panel')
            all_query_params = {}
            for param in valid_params:
                curr_param = params.get(param, None)
                if curr_param:
                    
                    curr_param = curr_param.strip()
                    list_params.append("{}={}".format(param, curr_param))
                    all_query_params[param] = curr_param
            def sp_query_builder(no_rangka=None, nama_panel=None, sisi_panel=None, sumber=None):

                # alias
                msp = aliased(MSparepartVin)

                fields = (msp.NOU,msp.NO_RANGKA,msp.KATEGORI_PART,msp.BAGIAN_PART,msp.NO_PART,
                            msp.NAMA_PART,msp.NAMA_PANEL,msp.SISI_PANEL,
                            msp.CODE,msp.NOTE,msp.QTY_REQUIRED,msp.PROD_DATE,msp.MODEL,msp.TRANSMISION,msp.NO_RANGKA_10D,
                            msp.TIPE,msp.LDR_ID,msp.LKB_ID,
                            msp.REF_ASSEMBLY,msp.REP_PART,msp.QTY_REP_PART,msp.SUMBER,msp.ID_LAMA,msp.ID_MODEL_COVERED
                        # , vin_tb.vin
                        )
                select_data = session.query(*fields)
                filtering = []
                if no_rangka:
                    filtering.append(msp.NO_RANGKA_10D.ilike('%{}%'.format(no_rangka.upper())))
                if nama_panel:
                    filtering.append(msp.NAMA_PANEL.ilike('%{}%'.format(nama_panel.upper())))
                if sisi_panel:
                    filtering.append(msp.SISI_PANEL.ilike('%{}%'.format(sisi_panel.upper())))
                if sisi_panel:
                    filtering.append(msp.SUMBER.ilike('%{}%'.format(sumber.upper())))
                filter_group = and_(*filtering).self_group()
                select_data = select_data.filter(filter_group)
                # data = 'apa'
                return select_data
            
            
            # def sp_run_query(limit, offset, no_rangka, nama_panel, sisi_panel):
            @cache_it(cache=my_cache, expire=60*60)
            def sp_run_query(no_rangka, nama_panel, sisi_panel, limit, offset):
                # result = sp_query_builder(**kwargs).limit(limit).offset(offset)
                # print(sp_query_builder(no_rangka,nama_panel,sisi_panel))
                result = sp_query_builder(no_rangka,nama_panel,sisi_panel).limit(limit).offset(offset)
                count = sp_query_builder(no_rangka,nama_panel,sisi_panel).count()
                retval = []
                for row_itm in result:
                    retval.append(row_itm)
                # print(retval)
                count_page=len(retval)
                return retval,count,count_page

            try:
                sumbers = get_sumber_from_sparepart()
                print(sumbers)
                data = []
                page = int(params.get('page', 1))
                limit = int(req.context['pagination']['limit'])
                offset = (page - 1) * limit
                data_sparepart,count,count_page = sp_run_query(no_rangka, nama_panel, sisi_panel, limit, offset)
                prev_page,next_page = None,None
                if count <= limit:
                    rows = count
                else:
                    rows = limit
                for row in range(count_page):
                    # print(data_sparepart[row][1])
                    objects = {}
                    fields = ('NOU', 'NO_RANGKA', 'KATEGORI_PART'
                            , 'BAGIAN_PART', 'NO_PART'
                            , 'NAMA_PART', 'NAMA_PANEL'
                            , 'SISI_PANEL', 'CODE', 'NOTE', 'QTY_REQUIRED', 'PROD_DATE', 'MODEL'
                            , 'TRANSMISION', 'NO_RANGKA_10D', 'TIPE', 'LDR_ID', 'LKB_ID', 'REF_ASSEMBLY', 'REP_PART'
                            , 'QTY_REP_PART', 'SUMBER', 'ID_LAMA', 'ID_MODEL_COVERED'
                            )
                    
                    for index, value in enumerate(fields):
                        objects[value] = data_sparepart[row][index]
                    
                    id_lama = data_sparepart[row][-2]
                    objects['img'] = get_image_ids(id_lama)
                    data.append(objects)
                    
                main_params = "/sparepart_search?"
                for para in list_params:
                    para = para.replace(' ','%20')
                    if list_params[len(list_params) - 1] == para:
                        main_params += para
                    else:
                        main_params += para + "&"
                print(limit,' ',count)
                total_page = math.ceil(count / limit)
                if page == 1:
                    prev_page = None
                else:
                    prev_page = "{0}&page={1}".format(main_params, page - 1)

                if page >= total_page:
                    next_page = None
                else :
                    next_page = "{0}&page={1}".format(main_params, page + 1)


                respon = {
                    "count": count,
                    "prev_page" : prev_page,
                    "next_page" : next_page,
                    "results": data
                }

                resp.body = json.dumps(respon, default=alchemyencoder)
                resp.status = falcon.HTTP_200

            except Exception as e:

                resp.body = json.dumps({'error': '{} - {}'.format(type(e), str(e))})
                resp.status = falcon.HTTP_500


@cache_it(cache=my_cache)
def get_image_ids(id_lama = None):
    

    # connection = cx_Oracle.Connection("oracle+cx_oracle://mbu:asmmbuapp05it@192.168.103.81:1521/OPASM1") 
    # cursor = connection.cursor() 
    # # connection = cx_Oracle.connect(user="mbu", password="asmmbuapp05it", dsn=my_dsn)
    # # cursor1 = connection.cursor()
    # select_data = """
    #         select id_image from M_LINK_IMG where id_sparepart = '{0}' 
    #     """.format(id_lama.upper())
    # a = cursor.execute(select_data)
    # idg = ""
    # d = []
    # for query in a:
    #     d.append('/image/?id_sparepart='+query[0])

    # return d

    result = []
    if not id_lama:
        return result

    with session_scope() as session:

        li = aliased(MsdTbLinkImageSparepart)
        image = session.query(li.ID_IMAGE) \
            .filter(li.ID_SPAREPART == id_lama)
        for res in image.all():
            link_image = "/image/?id_image={0}".format(res[0])
            result.append(link_image)
        # session.close()

        return result


# @lru_cache(maxsize=128)
# def get_co_occurrence(id_panel=None,id_model_covered=None,part_number=None):
#     result = "/co_occurrence/?id_panel={0}&id_model_covered={1}&part_number={2}".format(id_panel,id_model_covered,part_number)
#     return result

# @lru_cache(maxsize=128)
# def get_abbreviation(id_merek_kend = None):
#     result = "/abbreviation/{0}".format(id_merek_kend)
#     return result


@cache_it(cache=my_cache)
def get_sumber_from_sparepart():
    with session_scope() as session:
        sumbers = [itm[0] for itm in session.query(MSparepartVin.SUMBER).distinct()]
        sumbers.sort()
        return sumbers