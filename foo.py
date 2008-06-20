import sys
import os

sys.path.append('..')

from framework.Router import Router
from framework.Controller import controller


@controller
def hello(req):
    if req.method == 'POST':    
        return 'Hello %s!' % req.params['name']
    elif req.method == 'GET':
        return '''<form method="POST">
            Your name:<inpout type="text" name="name">
            <input type="submit">
            </form>'''

hello_world = Router()
hello_world.add_route('/', hello)
