import os
from decimal import Decimal
from .database import session_scope

class BaseResource(object):
    def __init__(self, scope=session_scope):
        self.session_scope = scope

    @staticmethod
    def default_encode(o):
        if isinstance(o, Decimal):
            return str(int(o))
        raise TypeError(repr(o) + " is not JSON serializable")