from Controllers import RestController

class _Hello:

    def __init__(self, req):
        self.request = req

    def get(self):
        return '''<form method="POST">Your Name
                    <input type="text" name="name">
                    <input type="submit"></form>'''
    
    def post(self):
        return 'Hello %s! The resident jollywaggler!' % self.request.params['name']

Hello = RestController(_Hello)
