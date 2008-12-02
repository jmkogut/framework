from framework.Applications import SOAPApplication, SOAPMethod

class HelloSOAP(SOAPApplication):
	
	@SOAPMethod
	def HelloTest(self):
		'''
		No SOAP docstring here, will default ReturnType to string
		and not allow any arguments. (This is desired behaviour).
		'''
		return "Hello, World!"

	@SOAPMethod
	def AddArgumentsAsString(self, num1, num2):
		'''
		Adds num1 to num2 and returns the value as a string phrase.

		##AddArguments:string, num1:long, num2:long
		'''
		return "The sum of %s and %s is %s" % (num1, num2, (num1 + num2))

	@SOAPMethod
	def AddArguments(self, num1, num2):
		'''
		Adds num1 to num2 and returns the value.

		##AddArguments:long, num1:long, num2:long
		'''
		return num1+num2

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
