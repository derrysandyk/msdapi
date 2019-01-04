import os
import falcon
# import prometheus_client
# from prometheus_client import make_wsgi_app
# from .utama import Resource
from .gambar import Images
# from .vin import Resource3
# from .suggestion import Resource4
from .sparepart_search import sparepart_search
# from .abbreviation import Abbreviation
# from .vin_new import VINResource
# from .inivincoba import VINResource2
# from .joincoba import JOINResource
# from .openimage import openimage2
# from .preconfig import coba123

# from .update_harga import Updateharga
# from .coocurent import coocurent
# from .vinnew import Vinnew
# from .vehicle_brand import vehicle_brand
# from .vehicle_model_search import vehicle_model
# from .vehicle_type_search import vehicle_type
# from .vehicle_transmission import vehicle_transmission
# from .vehicle_submit_search import vehicle_submit
from falcon_multipart.middleware import MultipartMiddleware
from .auth import AuthMiddleware
# api = application = falcon.API()
api = falcon.API(middleware=[MultipartMiddleware(), AuthMiddleware()])
# sparepart = Resource()
gambar = Images()
# vin=Resource3()
# vin2=Vinnew()
# suggestion=Resource4()
sparepart_search2=sparepart_search()
# abbreviation = Abbreviation()
# vin_new=VINResource()
# vin_new2=VINResource2()
# joinan=JOINResource()
# openih=openimage2()
# make=coba123()
# update= Updateharga()
# coocur= coocurent()
# brand = vehicle_brand()
# model = vehicle_model()
# types = vehicle_type()
# transmission = vehicle_transmission()
# submit = vehicle_submit()
# # api.add_route('/vin_code', vin)
# # api.add_route('/spareparts', sparepart)
api.add_route('/image', gambar)
# api.add_route('/suggestions', suggestion)
api.add_route('/sparepart_search', sparepart_search2)
# api.add_route('/abbreviation/{id_merek_kend}', abbreviation)
# api.add_route('/vin_newest', vin_new2)
# api.add_route('/join', joinan)
# api.add_route('/open_image', openih)
# api.add_route('/metrics' ,make)
# api.add_route('/update_harga' ,update)
# api.add_route('/co_occurrence' ,coocur)
#new API
# api.add_route('/vin_code_new', vin2)
# api.add_route('/vehicle_brand_search', brand)
# api.add_route('/vehicle_model_search', model)
# api.add_route('/vehicle_type_search', types)
# api.add_route('/vehicle_transmission_search', transmission)
# api.add_route('/vehicle_submit_search', submit)