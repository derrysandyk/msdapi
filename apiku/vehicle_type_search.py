import json
import falcon
import cx_Oracle
import collections
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor1 = connection.cursor()
class vehicle_type(object):
    def on_get(self, req, resp):
        params = req.params
        model = params.get('model', None)
        brand = params.get('brand', None)
        types = params.get('type', None)
        select_data = """
            select distinct transmission , engine from msd_tb_model_covered
            where grade = '{0}' and id_model_kend = (select id_model_kend from msd_tb_model_kend where model_kend = '{1}' 
                        and 
                            id_merek_kend = (select id_merek_kend from msd_tb_merek_kend where merek_kend = '{2}' ))
        """.format(types.upper(), model.upper(), brand.upper())
        a = cursor1.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["Transmission"] = query[0]
            d["Engine"] = query[1]
            objects_list.append(d)

        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        