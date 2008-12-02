#!/usr/bin/python

import sys, os
sys.path.append('/root/Projects/framework')

from framework.Router import Router
from examples.SOAPHelloApplication import HelloSOAP

from webob import Request, Response

def presp(resp):
	for line in resp.body.split("\n"):
		print ' << %s' % line

testRouter = Router();
testRouter.add_route('/soap-hello.*', HelloSOAP)

''' For testing (no requests made)
if __name__ == '__main__':

	print "Initializing requests"
	reqindex = Request.blank('/')
	reqmethod = Request.blank('/HelloTest')

	print "Printing response for /"
	presp(reqindex.get_response(testRouter))

	print "Printing response for /HelloTest"
	presp(reqmethod.get_response(testRouter))
'''

''' For wsgi / lightthpd '''
if __name__ == '__main__':
	from fcgi import WSGIServer
	
	application = testRouter

	os.setuid(33) # Set to www-data
	WSGIServer(application, bindAddress="/tmp/fcgi-app.sock").run()
