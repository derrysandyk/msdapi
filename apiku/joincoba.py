# -*- coding:utf-8 -*-
import falcon
import json
import logging
from .base import BaseResource
from .inis import sparepart,image
from .preconfig import c,REQUEST_TIME
logger = logging.getLogger()

class JOINResource(BaseResource):
    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        # params = req.params
        # vin = params.get('vin', None)
        # filterlagi = params.get('search', None)
        try:
            label_dict = {"method": "GET", "endpoint": "join"}
            c.labels(**label_dict).inc()
            with self.session_scope() as session:
                sparepartselected = sparepart.__table__.columns
                imageselected = image.__table__.columns
                #result = session.query(VINLAGI).with_entities(*selected_columns).filter(VINLAGI.no_mesin.ilike('%{}%'.format(filterlagi))).all()
                result = session.query(*sparepartselected,image.id,image.image_name).\
                    select_from(sparepart).\
                    join(image, sparepart.image_id == image.id).\
                    filter(sparepart.id <= 20).all()
                if result:
                    tampung=[]
                    for res in result:
                        tampung.append(res)
                    print([row._asdict() for row in result])
                    resp.body =json.dumps([ row._asdict() for row in result ])
                    resp.status = falcon.HTTP_200
                else:
                    resp.body = json.dumps({'error': True, 'message': 'VIN not found'})
                    resp.status = falcon.HTTP_200
        except Exception as e:
            message = '{} - {}'.format(type(e), str(e))
            logger.error(message)
            resp.body = json.dumps({'error': True, 'message': message})
            resp.status = falcon.HTTP_400
