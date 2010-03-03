from webob import Response

def Template(path, name, data=None, type='html'):
    if not path: path = ''

    file = path+(name+'.html' if not '.' in name else name)
    content = open(file).read()

    if data:
        for key in data:
            content = content.replace('{{%s}}'%key, data[key])

    return Response(body=content, content_type=('text/'+type))
