class tests:

    def log(self, source, msg):
        print '>> %s: %s' % (source.capitalize(), msg)

    def config(self, name):
        import Config.Routes
        import re

        totalroutes = len(Config.Routes.routes)
        goodroutes = 0

        for route in Config.Routes.routes:
            try:
                if route.startswith('/') and re.compile(route):
                    goodroutes += 1
            except:
                pass

        self.log(name, '%d/%d routes passed validation' % (goodroutes, totalroutes))


if __name__ == '__main__':
    
    try:        
        t = tests()
        run = (t.config,)

        for test in run:
            test(str(test.im_func).split(' ')[1])

    except:
        print "One or more tests failed."
        raise

else:
    raise Exception('Tests are not to be loaded, please run this by itself via python ./tests.py')
