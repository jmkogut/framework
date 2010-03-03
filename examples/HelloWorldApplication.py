import sys

sys.path.append('/home/potbot/projects/framework')

from framework.Router import Router
from framework.Controllers import Controller


@Controller
def hello(req):
    return 'Hello, World!<br />You called %s' % req.path_info


@Controller
def goodbye(req):
	return "Goodbye!"

routes = (
    ('^/gb', goodbye),
    ('.*', hello)
)

hello_world = Router()
for (route,handler) in routes:
    hello_world.add_route(route, handler)
