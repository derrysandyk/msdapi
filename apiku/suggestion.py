import json
import falcon
import cx_Oracle
import collections
import requests
from .preconfig import c,REQUEST_TIME
import time
my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
cursor = connection.cursor()
class Resource4(object):
    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        label_dict = {"method": "GET", "endpoint": "suggestions"}
        c.labels(**label_dict).inc()
        if "part_name" in req.params:
            result = requests.get('{}suggest_partname/select?q={}&rows=20'.format('http://192.168.105.102:1111/solr/', req.params['part_name']))
            data = result.json()
            try:
                retval = [x['part_name'] for x in data['response']['docs']]
                resp.body = json.dumps(retval)
            except IndexError:
                resp.body = json.dumps(None)
        elif "part_number" in  req.params:
            result = requests.get('{}suggest_partnumber/suggest?q={}&rows=20'.format('http://192.168.105.102:1111/solr/', req.params['part_number']))
            data = result.json()
            try:
                resp.body = json.dumps(data['spellcheck']['suggestions'][1]['suggestion'])
            except IndexError:
                resp.body = json.dumps(None)
        else:
            resp.body = json.dumps({'message': 'Server works!'})

        