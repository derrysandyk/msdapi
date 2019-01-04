from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time
import falcon

c = Counter('requests_for_host', 'Number of runs of the process_request method', ['method', 'endpoint'])
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
g = Gauge('my_inprogress_requests', 'Description of gauge')
d = Gauge('data_objects', 'Number of objects')
class coba123(object):
    def __init__(self):
        start_http_server(8889)
            # Generate some requests.
