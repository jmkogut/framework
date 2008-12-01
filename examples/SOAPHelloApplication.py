import re

import tempita

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

		if (self.request.path_info != ""):
			self.data['appname'] = self.request.path_info.lstrip('/').split('/')[0]
		else:
			self.data['appname'] = self.__module__.split('.').pop()

		self.data['namespace'] = self.request.host_url

	def getData(self, attr):
		mdata = {
			'name': attr,
			'arguments': [],
			'returntype': 'string'
		}
	
		doc = None
		for line in self.__getattribute__(attr).__doc__.split("\n"):
			if line.lstrip("\t").startswith('##'):
				doc = line.lstrip("\t#").split(", ")
		
		if doc:
			mdata['returntype'] = doc[0].split(':')[1]
			doc.remove(doc[0])
		
			if len(doc) > 0:
				for arg in doc:
					arg = arg.split(':')
					mdata['arguments'].append({'name':arg[0], 'type':arg[1]})
		else:
			mdata['returntype'] = "string"

		return mdata

	def index(self):
		return tempita.Template.from_filename('SOAP.WSDL.tmpl').substitute(self.data)

	def call(self):
		try:
			method = self.request.path_info.lstrip('/').split('?')[0]
			return self.__getattribute__(method)()
		except:
			return "OOPS"

	def issoapmethod(self, methodname):
		try:
			return self.__getattribute__(methodname).__issoapmethod__
		except AttributeError:
			return False


def SOAPMethod(func):
	func.__issoapmethod__ = True
	
	if (func.__doc__ == None): func.__doc__ = ""
	return func


class HelloSOAP(SOAPApplication):
	
	@SOAPMethod
	def HelloTest(self):
		return "Hello, World!"

	@SOAPMethod
	def AddArguments(self, num1, num2):
		'''
		##AddArguments:string, num1:long, num2:long
		'''
		return "The sum of %s and %s is %s" % (num1, num2, (num1 + num2))

	@SOAPMethod
	def DescribePerson(self, name, age, male):
		'''
		##DescribePerson:string, name:string, age:int, male:boolean
		'''
		
		if (male):
			gpronoun = "him"
		else:
			gpronoun = "her"

		return "%s, age %s, has a lot going for %s!" % \
			(name, age, gpronoun)

HelloSOAPTest = SOAPController(HelloSOAP)
