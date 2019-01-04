import json
import falcon
import cx_Oracle
import collections
from .preconfig import c,REQUEST_TIME
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor1 = connection.cursor()
class Vinnew(object):
    def on_get(self, req, resp):
        params = req.params
        vin_code = params.get('vin', None)
        select_data = """
        select merek.merek_kend, models.model_kend , vin.prod_from ,covered.grade, vin.transmission , covered.displacement from a_tb_vin vin 
            join msd_tb_model_covered covered
                on vin.id_model_covered = covered.id_model_covered
            join msd_tb_model_kend models
                on models.id_model_kend = covered.id_model_kend
            join msd_tb_merek_kend merek
                on merek.id_merek_kend = models.id_merek_kend
        where vin = '{0}'
        """.format(vin_code)
        a = cursor1.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["merk"] = query[0]
            d["models"] = query[1]
            d["year"] = query[2]
            d["type"] = query[3]
            d["transmission"] = query[4]
            d["engine capacity"] = query[5]
            objects_list.append(d)
            break

        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        