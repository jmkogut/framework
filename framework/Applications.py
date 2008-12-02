class Application(object):
	'''
	Base application, all sub-apps inherit from this.
	'''
	
	# The filename of the template
	template_name = None

	# A dict to pass to tempita, the templating engine.
	template_data = {}


class SOAPApplication(Application):
	'''
	Creates an easy to use way to expose a Python class to SOAP
	'''

	SOAPMethods = []

	def __init__(self, req):
		'''
		Constructor, sets up the SOAP Application for usage,
		determines which methods should be made available to the
		public, and sets up the local data store for the WSDL for
		this application.

		Arguments:
		webob.Request request -- A webob Request object
		'''

		self.request = req
		self.template_data['methods'] = []

		for attr in dir(self):
			if (self.is_soap_method(attr)):
				self.SOAPMethods.append(attr)
				self.template_data['methods'].append( self.getData(attr) )

		if (self.request.path_info != ""):
			self.template_data['appname'] = self.request.path_info.lstrip('/').split('/')[0]
		else:
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
			if line.lstrip("\s").startswith('##'):
				soap_doc = line.lstrip("\s#")
		
		# If we found a docstring, parse it for the given method arguments and returntype
		if soap_doc:
			soap_doc = soap_doc.split(', ')

			method_data['returntype'] = soap_doc[0].split(':')[1]
			soap_doc.remove(doc[0])
		
			if len(doc) > 0:
				for arg in doc:
					arg = arg.split(':')
					method_data['arguments'].append({'name':arg[0], 'type':arg[1]})
		else:
			method_data['returntype'] = "string"

		return method_data

	def index(self):
		'''
		A index method, lists the available SOAP methods in the
		WSDL format.
		'''
		
		# This doesn't need to setup template_data, as the constructor
		# does that for us, simply override template_name and we're good
		# to go.
		self.template_name = 'SOAP.WSDL.tmpl'

		return

	def call(self):
		'''
		Calls a method (supplied by the request uri).
		'''

		try:
			method = self.request.path_info.lstrip('/').split('?')[0]

			self.template_name = 'SOAP.Response.tmpl'
			self.template_data['soap_response'] = self.__getattribute__(method)()

			return
		except:
			return framework.Response.SOAPError

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
			return self.__getattribute__(methodname).__issoapmethod__
		except AttributeError:
			return False

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
