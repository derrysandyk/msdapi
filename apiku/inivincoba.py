# -*- coding:utf-8 -*-
import falcon
import json
import logging
from .base import BaseResource
from .inis import VINLAGI
from .preconfig import c,REQUEST_TIME,g,d
import random
import time
logger = logging.getLogger()

class VINResource2(BaseResource):
    @REQUEST_TIME.time()
    @g.track_inprogress()
    def on_get(self, req, resp):
        params = req.params
        vin = params.get('vin', None)
        filterlagi = params.get('search', None)
        try:
            label_dict = {"method": "GET", "endpoint": "vin_newest"}
            c.labels(**label_dict).inc()
            with self.session_scope() as session:
                selected_columns = VINLAGI.__table__.columns
                result = session.query(VINLAGI).with_entities(*selected_columns).filter(VINLAGI.no_mesin.ilike('%{}%'.format(filterlagi))).all()
                    #.filter(VINLAGI.no_rangka.like('%{}%'.format(vin)))\
                if result:
                    # data = result._asdict()
                    #resp.body = json.dumps(data, default=self.default_encode)
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
