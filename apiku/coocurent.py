import json
import falcon
import cx_Oracle
import collections
from .preconfig import c,REQUEST_TIME
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor = connection.cursor()
class coocurent(object):
    def on_get(self, req, resp):
        # vin_code = req.get_param("vin")
        params = req.params
        panel = params.get('nama_panel', None)
        select_data = """
            SELECT DISTINCT pm.indeks_lokasi
            from MSD_tb_panel_master s
            join tb_panel_matching_test2 pm
            on s.id_panel = pm.id_panel
            join tb_panel_alias_test g
            on pm.indeks_lokasi = g.indeks_lokasi
            where s.nama_panel = '{0}'
            """.format(panel.upper())
        a = cursor.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["indeks_lokasi"] = query[0]
            objects_list.append(d)
        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        