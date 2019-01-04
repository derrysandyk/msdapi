import json
import falcon
import cx_Oracle
import collections
from .preconfig import c,REQUEST_TIME
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor1 = connection.cursor()
class vehicle_brand(object):
    def on_get(self, req, resp):
        params = req.params
        brand = params.get('brand', None)
        select_data = """
            select distinct models.model_kend from msd_tb_model_kend models 
                where id_merek_kend = (select id_merek_kend from msd_tb_merek_kend where merek_kend = '{0}' ) 
        """.format(brand.upper())
        a = cursor1.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["model"] = query[0]
            objects_list.append(d)

        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        