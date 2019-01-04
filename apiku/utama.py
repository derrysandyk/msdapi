import json
import falcon
import cx_Oracle
import collections
from .preconfig import c,REQUEST_TIME
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor = connection.cursor()
class Resource(object):
    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        kunci,isi=list(()),list(())
        try:
            label_dict = {"method": "GET", "endpoint": "spareparts"}
            c.labels(**label_dict).inc()
            for key,value in req.params.items():
                kunci.append(key)
                isi.append(value)
            query_parameter=""
            for a in range(len(kunci)):
                if len(kunci)<1:
                    query_parameter=str(query_parameter)+str(kunci[a])+" = '"+str(isi[a])+"'"
                else:
                    if a==len(kunci)-1:
                        query_parameter=str(query_parameter)+str(kunci[a])+" = '"+str(isi[a])+"'"
                    else:
                        query_parameter=str(query_parameter)+str(kunci[a])+" = '"+str(isi[a])+"' AND "
            print(query_parameter)
            querynya = "SELECT id_spare ,up_to ,type ,rep ,part_no ,qty ,remarks ,spare_part_set FROM MITSUBISHI_PAJERO where "+query_parameter
            a = cursor.execute(querynya)
        except cx_Oracle.DatabaseError:
            querystring = "SELECT id_spare ,up_to ,type ,rep ,part_no ,qty ,remarks ,spare_part_set FROM MITSUBISHI_PAJERO"
            a = cursor.execute(querystring)
        global j
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["id"] = query[0]
            d["part_number"] = query[1]
            d["description"] = query[2]
            d["assembly_set"] = query[3]
            d["merk"] = query[4]
            d["model"] = query[5]
            d["source_url"] = query[6]
            d["image"] = query[7]
            objects_list.append(d)
        j = json.dumps(objects_list)
        resp.body = j
        #resp.body = data['file_image']
        resp.content_type = 'image/jpeg'
        resp.status = falcon.HTTP_200