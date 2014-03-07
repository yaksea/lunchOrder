#encoding=utf-8
'''
Created on 2012-5-3

@author: Administrator
'''
import tornado
import os
from lunchOrder.controller.handlers import default, HANDLER_ROOT
from tornado.web import RequestHandler
import sys
from lunchOrder import settings
import datetime

def getHandlers():    
    handlers = []
    __buildHandlers(handlers, "")
    handlers.extend([
                         (r'^/$', default.Default),
                     ])
    return handlers 



def __buildHandlers(handlers, path):
    curDir = os.path.join(HANDLER_ROOT, path).replace('\\', '/')
    innerPath = path
    for item in os.listdir(curDir):
        itemPath = os.path.join(curDir, item)
        if os.path.isfile(itemPath):
            info = os.path.splitext(item)
            if info[1] == '.py' and not info[0].startswith('_'):
                innerPath = os.path.join(path, info[0]).replace('\\', '/')
                moduleName = ('lunchOrder.controller.handlers.'+innerPath).replace('/','.')
                module = __import__(moduleName)
                module = sys.modules[moduleName]
                
                for attritude in dir(module):
                    cls = getattr(module, attritude)

                    if isinstance(cls, type) and issubclass(cls, RequestHandler):
                        classPath = (innerPath+'/'+attritude).lower()
                        if classPath.endswith('/default'):
                            classPath = classPath[:-8]
                            
                        handlers.append((r'^/'+classPath+'/?$', cls))
                        
                        
        elif os.path.isdir(itemPath):
            innerPath = os.path.join(path, item)
            __buildHandlers(handlers, innerPath)    

def run():
    _settings = {'template_path': os.path.join(os.path.dirname(__file__), 'templates'), 
                "static_path": settings.TND['static_path']}
    application = tornado.web.Application(getHandlers(), 
                                      debug=False, **_settings)
    application.listen(8020)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    run()
#    print os.path.dirname(__file__)
#    print os.curdir
#    print os.getcwd()
    