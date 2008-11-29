import sys
import os

sys.path.append('/root/Projects')

from framework.Router import Router
from framework.Controllers import Controller


@Controller
def hello(req):
    return 'Hello, World!<br />You called %s' % req.path_info


@Controller
def goodbye(req):
	return "Goodbye!"

hello_world = Router()
hello_world.add_route('^/gb', goodbye)
hello_world.add_route('.*', hello)
