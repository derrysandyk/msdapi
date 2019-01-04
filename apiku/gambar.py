import json
import falcon
import cx_Oracle
import collections
import base64
from .preconfig import c,REQUEST_TIME
# my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
# connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
# cursor = connection.cursor()
from .database import session_scope
from sqlalchemy.orm import aliased
from .base import BaseResource
from .inis import MsdTbImageSparepart , MsdTbLinkImageSparepart 
from .utils import alchemyencoder
from .auth import AuthMiddleware
class Images(BaseResource):
    def on_get(self, req, resp):

            # label_dict = {"method": "GET", "endpoint": "display_image"}
            # c.labels(**label_dict).inc()
        # my_dsn = cx_Oracle.makedsn("192.168.105.160",1521,service_name="DEV_DATABOT")
        # connection = cx_Oracle.connect(user="databot", password="oracle_Bot1", dsn=my_dsn)
        # cursor1 = connection.cursor()
        # id_sparepart = req.get_param("id_sparepart")
        # select_data = """
        #         select file_image from msd_tb_link_image_sparepart lsp
        #         join msd_tb_image_sparepart isp on isp.id_image = lsp.id_image 
        #         where lsp.id_sparepart = '{0}' 
        #     """.format(id_sparepart)
        # a = cursor1.execute(select_data)
        # blob = ""
        # for query in a:
        #     # print(query[0].open())
        #     blob = query[0].read()
        #     print(blob)

        # resp.body = blob
        # resp.content_type = 'image/jpg'
        # resp.status = falcon.HTTP_200
        with self.session_scope() as session:

            params = req.params
            id_image = params.get('id_image', None)
            # open_image ="""
            #         select file_image from msd_tb_sparepart sp
            #             join msd_tb_link_image_sparepart li on sp.ID_SPAREPART = li.ID_SPAREPART
            #             join msd_tb_image_sparepart isp on isp.ID_IMAGE = li.ID_IMAGE
            #         where isp.id_image = '{0}'
            #                 """.format(id_image)
            isp = aliased(MsdTbImageSparepart)
            open_image = session.query(isp.IMAGE)\
                .filter(isp.ID_IMAGE == '{}'.format(id_image)).first()

            # print(open_image[0])
            # for row in open_image :
                # print(open_image)
            # a = cursor.execute(open_image)
            # blob = ""
            # for query in a:
            #     imageBlob = query[0]
            #     blob= imageBlob.read()
            #     break
            # imageBlob = query[0]
            # blob= imageBlob.read()
            # resp.body = open_image[0]
            # gambar = {
            #     'ini' : 'gambar'
            # }
            # resp.body = blob
            resp.body = json.dumps(open_image[0])
            # resp.content_type = 'image/jpg'
            resp.status = falcon.HTTP_200