'''
Created on 2012-12-13

@author: Administrator
'''
from tornado.web import RequestHandler
from lunchOrder.logMonitor.handlers import allow_ips
import json
import traceback
import functools
import tornado
from lunchOrder.common.tnd.params import Params
from lunchOrder import settings

def secure(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):      
        if settings.ENVIRONMENT['production'] and self.get_cookie('secure_key') != 'toukandaimashiwugui':
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
    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)   
        self._params = None 
        self.modules = {}
        self.blocks = {}
        self.fields = {}
    
    @secure   
    def get(self):
        self.write('nothing')
    
    @secure   
    def post(self):
        self.write('nothing')
                         
    def sendMsg(self, message='success', statusCode=200, **kwargs):
        msg = dict(message=message,statusCode=statusCode)
        msg.update(kwargs)
        self.write(json.dumps(msg))

    @property
    def params(self):
        if not self._params:
            self._params = Params()
            for argName in self.request.arguments:
                args = self.get_arguments(argName)
                if len(args)>1:
                    self._params[argName] = args
                else:
                    self._params[argName] = args[0]
                    
            if self.request.method.upper() == 'POST':
                try:
                    self._params.update(json.loads(self.request.body))
                except:
                    pass
                                
        return self._params 
    
#    @tornado.web.asynchronous   
#    def timeout(self):
#        self.send_error(408)
#        self.finish()




if __name__ == '__main__':
    pass