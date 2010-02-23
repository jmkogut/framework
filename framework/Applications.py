import sys
import traceback

from webob import Request, Response
from webob import exc

import tempita

import framework
from framework import Templates

class Application(framework.Base):
	'''
	Base application, all sub-apps inherit from this.
	'''
	
	template_name = None
	Template = None

	# A dict to pass to tempita, the templating engine.
	template_data = {
		'method':{}
	}


class SOAPApplication(Application):
	'''
	Creates an easy to use way to expose a Python class to SOAP
	'''

	SOAPMethods = []

	def __init__(self, environ, start_response):
		'''
		Constructor, sets up the SOAP Application for usage,
		determines which methods should be made available to the
		public, and sets up the local data store for the WSDL for
		this application.
		'''
		self.request =  Request(environ)
		self.environ = environ
		self.start_response = start_response

		self.template_data['methods'] = []

		for attr in dir(self):
			if (self.is_soap_method(attr)):
				self.debug('Found SOAP Method: %s' % attr)
				self.SOAPMethods.append(attr)
				self.template_data['methods'].append( self.get_data_for_method(attr) )

		self.template_data['appname'] = self.__module__.split('.').pop()

		self.template_data['namespace'] = self.request.host_url

	def get_data_for_method(self, method):
		'''
		Takes a method name, finds it in self, and parses an (optional)
		docstring to format information to supply to the WSDL.

		Arguments:
		string method -- A method name
		'''

		method_data = {
			'name': method,
			'arguments': [],
			'returntype': 'string'
		}
	
		soap_doc = None

		# For each line in the given method's docstring
		for line in self.__getattribute__(method).__doc__.split("\n"):
			# Try to find a SOAP docstring
			if line.lstrip("\s\t").startswith('##'):
				soap_doc = line.lstrip("\s\t#")
		
		# If we found a docstring, parse it for the given method arguments and returntype
		if soap_doc:
			soap_doc = soap_doc.split(', ')
			self.debug('\tSOAP docstring: %s' % soap_doc)

			method_data['returntype'] = soap_doc[0].split(':')[1]
			soap_doc.remove(soap_doc[0])
		
			if len(soap_doc) > 0:
				for arg in soap_doc:
					arg = arg.split(':')
					method_data['arguments'].append({'name':arg[0], 'type':arg[1]})
		else:
			method_data['returntype'] = "string"

		return method_data

	def _call(self):
		'''
		Calls a method (supplied by the request uri).
		'''

		try:
			
			if 'HTTP_SOAPACTION' in self.request.environ:
				self.debug('SOAP ACTION REQEST: %s' % self.request.environ['HTTP_SOAPACTION'])
				#self.debug('SOAP REQUEST: %s' % self.request.body)
			
				method = self.request.environ['HTTP_SOAPACTION'].split('/').pop().rstrip('"')
				self.debug('SOAP Method is %s' % method)
			else:
				method = ''


			if method in [None, '', 'index']:
				#arguments = self.parse_soap_request()
				self.template_body = Templates.SOAP.WSDL
			
			else:
				self.template_body = Templates.SOAP.Response
				#self.debug(self.request)
				#arguments = self.parse_soap_request()
				arguments = {}
				self.template_data['method']['response'] = self.__getattribute__(method)(**arguments)
			
			self.template_data['method']['name'] = method
			return self.render()
		except:
			print "EXCEPTION"
			print traceback.format_exc()

	def render(self):
		'''
		Renders the template data to the template

		Returns: the result
		'''
		
		if self.template_name and not self.Template:
			self.debug('Instantiating template from filename: %s' % self.template_name)
			self.Template = tempita.Template.from_filename(self.template_name)
		
		if self.template_body and not self.Template:
			self.debug('Instantiating template from body...')
			self.Template = tempita.Template(self.template_body)

		self.debug('Using template data: %s' % self.template_data, False)
		return self.Template.substitute(self.template_data)


	def is_soap_method(self, method):
		'''
		Checks to see if the method is a SOAP method,
		determined by a property set by SOAPMethod decorator.

		Arguments:
		string method -- The name of the method in question

		Returns:
		bool is_soap_method -- Whether or not this method is a SOAP method
		'''

		try:
			return self.__getattribute__(method).__issoapmethod__
		except AttributeError:
			return False

	def handle(self, match):
		'''
		Takes the request from the router and handles it accordingly

		Required Group:
		SOAPMethod
		'''

		try:

			response = self._call()
			self.debug('SOAP Response was %s' % (response), False)
		
			if isinstance(response, basestring):
				self.debug('SOAP Application response was a string, building response from it')
				response = Response(body=response)
			else:
				self.debug('SOAP Application response was a Response object')

		except exc.HTTPException, e:
			self.debug('SOAP Application threw HTTPException')
			response = e
		
		response.content_type = 'text/xml'
		return response(self.environ, self.start_response)


def SOAPMethod(func):
	'''
	A decorator to be used on class methods to indicate to
	the host application that this method is a SOAP method.

	NOTE: Requires a line in the docstring with this format
	##MethodName:ReturnType, Arg1Name:Arg1ReturnType, Arg2Name:Arg2ReturnType, [...]

	Otherwise, the ReturnType is assumed to be string, and no arguments will be passed
	to the method.

	Examples:
	##GetTimeOfDay:datetime
	##AddNumbers:long, firstnum:long, secondnum:long
	##CreateUser:bool, email:string, password:string, address:string, age:int

	Returns:
	The decorated func.
	'''

	func.__issoapmethod__ = True
	
	if (func.__doc__ == None): func.__doc__ = ""
	return func
