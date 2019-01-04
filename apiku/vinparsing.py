# -*- coding:utf-8 -*-
import falcon
import json
import logging
from .base import BaseResource
from .inis import VIN

logger = logging.getLogger()


class VINResource(BaseResource):
    def on_get(self, req, resp):
        params = req.params
        vin = params.get('vin', None)
        print(vin)
        try:
            with self.session_scope() as session:
                selected_columns = VIN.__table__.columns
                result = session.query(VIN).with_entities(*selected_columns).filter(VIN.no_rangka.like('%{}%'.format(vin))).first()
                if result:
                    data = result._asdict()
                    resp.body = json.dumps(data, default=self.default_encode)
                    resp.status = falcon.HTTP_200
                else:
                    resp.body = json.dumps({'error': True, 'message': 'VIN not found'})
                    resp.status = falcon.HTTP_200
        except Exception as e:
            message = '{} - {}'.format(type(e), str(e))
            logger.error(message)
            resp.body = json.dumps({'error': True, 'message': message})
            resp.status = falcon.HTTP_400
