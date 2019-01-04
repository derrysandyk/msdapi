import json
import falcon
import requests
import cx_Oracle
import collections
from datetime import datetime
from sqlalchemy import and_, or_, between, func , Integer, cast, Numeric, Integer
from sqlalchemy.sql.expression import insert
from sqlalchemy.orm import aliased
from .auth import AuthMiddleware as am
from .inis import MsdTbMerekKend, MsdTbModelCovered, MsdTbModelKend, MsdTbSparepart, MsdTbHarga, ScrapingJob\
    , SparepartDaihatsu, SparepartIsuzu, SparepartMegazip, SparepartParts, SparepartSuzuki
from sqlalchemy import func
from .utils import alchemyencoder
from .base import BaseResource
TABLE_MAPPING = {
    'isuzu': SparepartIsuzu,
    'daihatsu': SparepartDaihatsu,
    'suzuki': SparepartSuzuki,
    'megazip': SparepartMegazip,
    'parts.com': SparepartParts,
}
CURRENCY_MAPPING = {
    'isuzu': 'IDR',
    'daihatsu': 'IDR',
    'suzuki': 'IDR',
    'megazip': 'USD',
    'parts.com': 'USD'
}
class Updateharga(BaseResource):
    def on_post(self, req, resp):
        with self.session_scope() as session:
            job_id = req.get_param("job_id")
            website = req.get_param("website")
            print('req', req.params)

            # alias
            cr = aliased(TABLE_MAPPING[website])
            sp = aliased(MsdTbSparepart)
            mc = aliased(MsdTbModelCovered)
            mdl = aliased(MsdTbModelKend)
            merek = aliased(MsdTbMerekKend)

            # get last_update time
            crawl_job = session.query(ScrapingJob.finish).filter(ScrapingJob.id == job_id)
            last_update = crawl_job.scalar()
            if not last_update:
                last_update = datetime.now()

            crawl = session.query(cr.part_number,cr.price, cr.merk) \
                .filter(and_(cr.job_id == job_id, cr.price.isnot(None))).subquery()
            print('ini',crawl)
            print('1')
            msd = session.query(sp.id_sparepart, func.to_number(func.replace(crawl.columns.price, '$', ''), '99999999999999.99'))\
                .add_columns('\'{}\' as currency'.format(CURRENCY_MAPPING[website])) \
                .add_columns('\'WEBSITE {}\' as sumber'.format(website.upper())) \
                .add_columns('TO_TIMESTAMP(\'{}\',\'YYYY-MM-DD HH24:MI:SS.FF\')'.format(last_update)) \
                .distinct() \
                .join(mc, sp.id_model_covered == mc.id_model_covered) \
                .join(mdl, mc.id_model_kend == mdl.id_model_kend) \
                .join(merek, merek.id_merek_kend == mdl.id_merek_kend)\
            
            print(msd)
            print('2')
            result = msd.join(crawl, sp.part_number == crawl.columns.part_number)\
                .filter(func.lower(merek.merek_kend) == func.lower(crawl.columns.merk))\
                .filter(sp.sumber == '\'WEBSITE {}\''.format(website.upper()))
            print(result)
            print('3')
            count = result.count()
            status = 'Failed'
            respon = {}
            if count > 0 :
                try:
                    insert_columns = (MsdTbHarga.id_sparepart, MsdTbHarga.harga, MsdTbHarga.currency, MsdTbHarga.sumber
                                    , MsdTbHarga.last_update)
                    session.execute(insert(MsdTbHarga).from_select(insert_columns, result))
                    session.commit()
                    status = 'Success'
                except Exception as e:
                    print('{} - {}'.format(type(e), str(e)))

                respon = {
                    'Status': status,
                    'Rows Affected': '{0}'.format(count)
                }
            else :
                respon = {
                    'Status' : status
                }
                print(result)
            resp.body = json.dumps(respon, default=alchemyencoder)
            resp.status = falcon.HTTP_200
