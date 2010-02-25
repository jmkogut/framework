from webob import Request, Response
from webob import exc

import simplejson

def Controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        
        if isinstance(resp, basestring):
            resp = Response(body=resp)

        return resp(environ, start_response)
    return replacement

def JSONController(func):
    """
    Copy of @Controller that returns jsonified results
    """
    def replacement(environ, start_response, **kwargs):
        req = Request(environ)
        try:
            resp = {'response': func(req, **kwargs)}
        except exc.HTTPException, e:
            resp = {'error': e}
        
        resp = Response(body=simplejson.dumps(resp))

        return resp(environ, start_response)
    return replacement



def RestController(cls):
    def replacement(environ, start_response):
        req = Request(environ)

        try:
            instance = cls(req, **req.urlvars)
            action = req.urlvars.get('action')

            if action:
                action += '_' + req.method.lower()
            else:
                action  = req.method.lower()
            
            try:
                method = getattr(instance, action)
            except AttributeError:
                raise exc.HTTPNotFound("No action %s" % action)

            resp = method()
            if isinstance(resp, basestring):
                resp = Response(body=resp)
        except exc.HTTPException, e:
            resp = e

        return resp(environ, start_response)
    return replacement
