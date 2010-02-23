#!/usr/bin/python

import sys, os
sys.path.append('/home/potbot/projects/framework')

from framework.Router import Router
from examples.SOAPHelloApplication import HelloSOAP
from examples.HelloWorldApplication import hello_world
from webob import Request, Response

def presp(resp):
    for line in resp.body.split("\n"):
        print ' << %s' % line

wsgiRouter = Router();
wsgiRouter.add_route('/soap-hello.*', HelloSOAP)

''' For testing (no requests made)
if __name__ == '__main__':

    print "Initializing requests"
    reqindex = Request.blank('/')
    reqmethod = Request.blank('/HelloTest')

    print "Printing response for /"
    presp(reqindex.get_response(wsgiRouter))

    print "Printing response for /HelloTest"
    presp(reqmethod.get_response(wsgiRouter))
'''

''' For wsgi / lightthpd '''
if __name__ == '__main__':
    #application = wsgiRouter
    application = hello_world
    
    from paste import httpserver
    httpserver.serve(application, host='0.0.0.0', port='8080')

    #from fcgi import WSGIServer
    #os.setuid(33) # Set to www-data
    #WSGIServer(application, bindAddress="/tmp/fcgi-app.sock").run()
