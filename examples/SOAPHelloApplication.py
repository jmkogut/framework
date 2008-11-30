import re
from framework.Controllers import SOAPController

class SOAPApplication(object):
	SOAPMethods = []
	data = {
		'methods': []
	}

	def __init__(self, req):
		self.request = req

		for attr in dir(self):
			if (self.issoapmethod(attr)):
				self.SOAPMethods.append(attr)
				self.data['methods'].append( self.getData(attr) )

		self.data['appname'] = self.__module__
		self.data['namespace'] = self.request.host_url

	def getData(self, attr):
		mdata = {
			'name': attr,
			'arguments': [],
			'returntype': 'string'
		}

		doc = self.__getattribute__(attr).__doc__
		for line in doc.split("\n"):
			if line.lstrip("\t").startswith('##'): doc = line.lstrip("\t#").split(", ")
		print doc

		return mdata

	def index(self):		
		return ', '.join(["%s" % (i) for i in self.SOAPMethods]).rstrip(', ')

	def call(self):
		method = self.request.path_info.lstrip('/').split('?')[0]
		return self.__getattribute__(method)()

	def issoapmethod(self, methodname):
		try:
			return self.__getattribute__(methodname).__issoapmethod__
		except AttributeError:
			return False


def SOAPMethod(func):
	func.__issoapmethod__ = True
	return func


class SOAPHelloApplication(SOAPApplication):
	
	@SOAPMethod
	def HelloTest(self):
		'''
		##HelloTest:string
		'''
		return "Hello, World!"

	@SOAPMethod
	def AddArguments(self, num1, num2):
		'''
		##AddArguments:string, num1:integer, num2:integer
		'''
		return "The sum of %s and %s is %s" % (num1, num2, (num1 + num2))

	@SOAPMethod
	def DescribePerson(self, name, age, male):
		'''
		##DescribePerson:string, name:string, age:integer, male:boolean
		'''
		
		if (male):
			gpronoun = "him"
		else:
			gpronoun = "her"

		return "%s, age %s, has a lot going for %s!" % \
			(name, age, gpronoun)

SOAPHello = SOAPController(SOAPHelloApplication)
