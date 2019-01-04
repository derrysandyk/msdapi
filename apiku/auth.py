import falcon


class AuthMiddleware(object):

    def __init__(self):
        pass
    def process_request(self, req, resp):
        auth_header = req.get_header('Authorization')
        if auth_header:
            req.context['authenticated'] = auth_header.split(' ')[-1] == 'dXNlcm5hbWU6cGFzc3dvcmQ='


    def validate_auth(req, resp, resource, params):
        description = 'Please provide valid authentication header.'
        challenges = ['Authorization: Basic ...']
        if 'authenticated' not in req.context or not req.context['authenticated']:
            raise falcon.HTTPUnauthorized('Authentication required',
                                        description,
                                        challenges,
                                        href='http://docs.example.com/auth')