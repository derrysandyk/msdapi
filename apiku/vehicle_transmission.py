import json
import falcon
import cx_Oracle
import collections
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor1 = connection.cursor()
class vehicle_transmission(object):
    def on_get(self, req, resp):
        params = req.params
        model = params.get('model', None)
        brand = params.get('brand', None)
        types = params.get('type', None)
        transmission = params.get('transmission', None)
        select_data = """
            select distinct prod_from,displacement from msd_tb_model_covered
                where grade = '{0}' and transmission = '{1}' and id_model_kend = (select id_model_kend from msd_tb_model_kend where model_kend = '{2}' 
                            and 
                                id_merek_kend = (select id_merek_kend from msd_tb_merek_kend where merek_kend = '{3}' ))
        """.format(types.upper(), transmission.upper(), model.upper(), brand.upper())
        a = cursor1.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["grade"] = query[0]
            objects_list.append(d)

        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        