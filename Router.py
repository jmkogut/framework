from Config import Routes

import re

from webob import Request
from webob import exc

class Router():

    def __init__(self):
        self.routes = []
        self.add_routes()

    def add_routes(self):
        for route in Config.Routes.routes:

            controller = route[1]
            if isinstance(controller, basestring)
                controller = self.load(controller)
            
            self.routes.append((re.compile(route[0]), controller)

    def load(self, controller):
        mod, func = controller.split(':', 1)

        __import__(mod)
        mod = sys.modules[mod]
        
        return getattr(mod, func)

    def __call__(self, environ, start_response):
        req = Request(environ)

        for route, controller in self.routes:
            if route.match(req.pattern_info):
                return controller(environ, start_response)
            
            return exc.HTTPNotFound()(environ, start_response)
