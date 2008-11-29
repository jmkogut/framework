#!/usr/bin/python

import sys, os
sys.path.append("/root/Projects")
sys.path.append("..")

from fcgi import WSGIServer

from HelloWorldApplication import hello_world
myapp = hello_world

if __name__ == "__main__":
	os.setuid(33) # Set to www-data
	WSGIServer(myapp, bindAddress="/tmp/fcgi-app.sock").run()
