from distutils.core import setup

# Configuration
APPNAME = 'framework'
VERSION = '0.01a'
AUTHOR = 'Joshua Kogut'
AUTHOR_EMAIL = 'joshua.kogut@gmail.com'

PROJECT_WEB = 'http://github.com/jmkogut/framework'

SHORT_DESCRIPTION = 'A generic WSGI-based framework.'
LONG_DESCRIPTION = '%s Project home at %s' % (SHORT_DESCRIPTION, PROJECT_WEB)

PACKAGES = ['framework']
PACKAGE_DATA = {
	'framework': ['Config/*']
}

# Setup
setup(
	name=APPNAME,
	version = VERSION,
	description = SHORT_DESCRIPTION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	url = PROJECT_WEB,
	packages = PACKAGES,
	package_data = PACKAGE_DATA,
	long_description = LONG_DESCRIPTION
)
