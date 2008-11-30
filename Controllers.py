from webob import Request, Response
from webob import exc

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


def SOAPController(SOAPMethods):
	def replacement(environ, start_response):
		req = Request(environ)

		try:
			instance = SOAPMethods(req, **req.urlvars)
			
			print " -- Path info was %s" % req.path_info
			if (req.path_info == "" or req.path_info == "/"):
				method = getattr(instance, "index")
			else:
				method = getattr(instance, "call")
			
			resp = method()
			if isinstance(resp, basestring):
				resp = Response(body=resp)

		except exc.HTTPException, e:
			resp = e

		return resp(environ, start_response)
	return replacement
