class Base(object):

	debug_app = False
	debug_verbose = False

	def debug(self, message, essential=True):
		'''
		Prints debug messages as long as debug_app is True.
		'''

		if self.debug_app and essential:
			print message
