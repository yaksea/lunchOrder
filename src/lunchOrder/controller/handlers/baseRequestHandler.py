'''
Created on 2012-12-13

@author: Administrator
'''
from tornado.web import RequestHandler
from lunchOrder.controller.handlers import allow_ips
import json
import traceback
import functools
import tornado
from lunchOrder import settings

def secure(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  
        
        if settings.ENVIRONMENT['production']:    
            if self.get_cookie('secure_key') != 'toukandaimashiwugui':
                self.send_error(404)
                return
                
        try:
            return method(self, *args, **kwargs)
        except Exception, ex:
            traceback.print_exc()
            errMsg = "%s\r\n%s"%(str(ex), traceback.format_exc())
            self.write(errMsg)            
            
    return wrapper  

class BaseRequestHandler(RequestHandler): 
    @secure   
    def get(self):
        self.write('nothing')
    
    @secure   
    def post(self):
        self.write('nothing')
                         
    def sendMsg(self, message, statusCode=200, *args, **kwargs):
        msg = dict(message=message,statusCode=statusCode)
        self.write(json.dumps(msg))
    
#    @tornado.web.asynchronous   
#    def timeout(self):
#        self.send_error(408)
#        self.finish()




if __name__ == '__main__':
    pass