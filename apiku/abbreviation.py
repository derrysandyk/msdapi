import falcon
import json
from .database import session_scope
from sqlalchemy import func
from sqlalchemy.orm import aliased
from .base import BaseResource
from .inis import MsdTbAbbreviation
from .utils import alchemyencoder
from .rediscache import my_cache,cache_it_json, cache_it
class Abbreviation(BaseResource):
    def on_get(self, req, resp, id_merek_kend):
        with self.session_scope() as session:
            # print(id_merek_kend)
            # response = [
            #                 { "ABS": "Antilock Brake System" },
            #                 { "BD": "Brake Force Distribution" }
            #             ]
            @cache_it(cache=my_cache, expire=60*10)
            def query_builder(id_merek=None):
                abb = aliased(MsdTbAbbreviation)
                select_data = session.query(abb.mark , abb.definition)\
                    .filter(func.replace(abb.id_merek_kend,' ','') == '{}'.format(id_merek)).all()
                return select_data
                # .filter(abb.id_merek_kend.ilike('%{}%'.format(id_merek_kend))).all()
            # print(select_data)

            data = {}
            objects = []
            list_data = query_builder(id_merek_kend)
            for ind, val in list_data :
                data[ind] = val
            objects.append(data)
            # data = select_data
            # result = {'status': task_result.status, 'result': task_result.result}
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(objects, default=alchemyencoder)