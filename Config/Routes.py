"""
    Routes configuration files, it's a regex:controller pair, pretty
    simple, really. I promise.
"""

routes = (
    #('/', 'controllers:index'),

    #('/(?P<year>\d\d\d\d)/', 'controllers:archive'),              # controllers:archive would be passed a four digit year
    #('/(?P<year>\d\d\d\d)/(?P<name>\w+)/', 'controllers:person'), # controllers:person would be passed the year and person
)
