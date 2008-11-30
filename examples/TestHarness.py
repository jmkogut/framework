#!/usr/bin/python

import sys
sys.path.append('../../')

from framework.Router import Router
from framework.examples.SOAPHelloApplication import SOAPHello

from webob import Request, Response

def presp(resp):
	for line in resp.body.split("\n"):
		print ' << %s' % line

if __name__ == '__main__':

	testRouter = Router();
	testRouter.add_route('.*', SOAPHello)

	print "Initializing requests"
	reqindex = Request.blank('/')
	reqmethod = Request.blank('/HelloTest')

	print "Printing response for /"
	presp(reqindex.get_response(testRouter))

	print "Printing response for /HelloTest"
	presp(reqmethod.get_response(testRouter))
