#-*- coding:utf-8 -*-
#from bs.main import getHandlers

#def app(environ, start_response):
#    status = '200 OK'
#    headers = [('Content-type', 'text/html')]
#    start_response(status, headers)
#    body=["Welcome to Baidu Cloud!\n"]
#    return body

 
import tornado.wsgi
from bs.handlers import upload
 
handlers = [
            (r'/', upload.MainHandler),
            (r'yy$', upload.MainHandler)
            ]
 
app = tornado.wsgi.WSGIApplication(handlers)
 

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)