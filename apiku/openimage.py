import json
import falcon
import logging
from .base import BaseResource
# from .inis import image
from .preconfig import c,REQUEST_TIME
logger = logging.getLogger()
class openimage2(BaseResource):
    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        try:
            label_dict = {"method": "GET", "endpoint": "open_image"}
            c.labels(**label_dict).inc()
            with self.session_scope() as session:
                imageselected = image.__table__.columns
                params = req.params
                imageid = params.get('image', None)
                #result = session.query(VINLAGI).with_entities(*selected_columns).filter(VINLAGI.no_mesin.ilike('%{}%'.format(filterlagi))).all()
                result = session.query(*imageselected).\
                    select_from(image).\
                    filter(image.id == imageid ).all()
                if result:
                    tampung=[]
                    for res in result:
                        tampung.append(res)
                    # print(tampung[1])
                    imageBlob = tampung[1]
                    resp.body = imageBlob
                    resp.content_type = 'image/jpg'
                    resp.status = falcon.HTTP_200
                    # resp.body =json.dumps([ row._asdict() for row in result ])
                    # resp.status = falcon.HTTP_200
                else:
                    resp.body = json.dumps({'error': True, 'message': 'VIN not found'})
                    resp.status = falcon.HTTP_200
        except Exception as e:
            message = '{} - {}'.format(type(e), str(e))
            logger.error(message)
            resp.body = json.dumps({'error': True, 'message': message})
            resp.status = falcon.HTTP_400