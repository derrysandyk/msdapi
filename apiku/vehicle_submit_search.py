import json
import falcon
import cx_Oracle
import collections
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor1 = connection.cursor()
class vehicle_submit(object):
    def on_get(self, req, resp):
        params = req.params
        model = params.get('model', None)
        brand = params.get('brand', None)
        types = params.get('type', None)
        prod_year = params.get('prodyear', None)
        engine = params.get('enginecapacity', None)
        transmission = params.get('transmission', None)
        select_data = """
        select  distinct asse.assembly_set, gr.group_part from msd_tb_sparepart sp
            join msd_tb_grouping gr
                on gr.id_group_part = sp.id_group_part
            join msd_tb_assembly_set asse
                on asse.id_assembly_set = sp.id_assembly_set
            where sp.id_model_covered in 
            (
            select distinct id_model_covered from msd_tb_model_covered
                    where grade = '{0}' and transmission = '{1}' and prod_from = '{2}' and displacement = '{3}' 
                        and id_model_kend = (select id_model_kend from msd_tb_model_kend where model_kend = '{4}' 
                                and 
                                    id_merek_kend = (select id_merek_kend from msd_tb_merek_kend where merek_kend = '{5}' ))
                                    )
        """.format(types.upper(), transmission.upper(),prod_year,engine.upper(), model.upper(), brand.upper())
        a = cursor1.execute(select_data)
        objects_list = []
        for query in a:
            d = collections.OrderedDict()
            d["part_function"] = query[1]
            d["part_assembly"] = query[0]
            objects_list.append(d)

        resp.body = json.dumps(objects_list)                
        resp.status = falcon.HTTP_200
        
        