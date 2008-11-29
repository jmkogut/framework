from framework.Config import Routes

import re
import sys

from webob import Request
from webob import exc

class Router:

    def __init__(self):
        self.routes = []
        self.add_routes()

    def add_route(self, route, controller):
        if isinstance(controller, basestring):
            controller = self.load(controller)
        
        route = '%s' % route.replace('@', '\\@')
        self.routes.append((route, controller))

    def add_routes(self):
        for route in Routes.routes:
            self.add_route(route[0], route[1])

    def load(self, controller):
        #print controller.split(':', 1)
        mod, func = controller.split(':', 1)

        __import__(mod)
        mod = sys.modules[mod]
        
        return getattr(mod, func)

    def __call__(self, environ, start_response):
        req = Request(environ)
        req.path_info = req.environ['REQUEST_URI'] # To work around lighttpd's failure to comply with WSGI

        for route, controller in self.routes:
            if re.match(route, req.path_info):
                print "route matched %s to %s" % (req.path_info, route)
                return controller(environ, start_response)
            
        print "Out of %s routes, nothing found to match %s" % (len(self.routes), req.path_info)
        return exc.HTTPNotFound()(environ, start_response)
