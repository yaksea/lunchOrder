#encoding=utf-8
'''
Created on 2012-9-23

@author: Administrator
'''

import functools
from lunchOrder.common.exception import StopOnPurpose
from lunchOrder.base.handlers.sessionHandler import SessionRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
import traceback
from lunchOrder.common import log
from lunchOrder.base.handlers.logHandler import LogRequestHandler
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
#from lunchOrder.base.handlers.encryptHandler import EncryptRequestHandler

        
def authenticate(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  
        mr = None    
        if not isinstance(self, SessionRequestHandler):
            mr = method(self, *args, **kwargs) 
        try:
            
            if not self.identity:                       
                if isinstance(self, PageRequestHandler)and self.request.method =='GET':
                    self.gotoLogin()
                elif isinstance(self, JsonRequestHandler):
                    self.sendMsg_NoIdentity('验证过期')            
                        
            mr = method(self, *args, **kwargs)
                        
        except StopOnPurpose:
            if not self._finished:
                self.finish()
        except:
            if isinstance(self, LogRequestHandler):
                self.log_error(traceback.format_exc())
                         
            log.error()
            try:
#                if isinstance(self, PageRequestHandler) and method.func_name=='get':
#                    self.gotoError()
#                el
                if isinstance(self, JsonRequestHandler):
                    self.sendMsg_Unknown()
            except StopOnPurpose:
                if not self._finished:
                    self.finish()
                    
        if isinstance(self, LogRequestHandler):
            self.log_flush()
        return mr            

            
    return wrapper
  
def admin(method):
    return specialRole(method, 'admin')       
       
def founder(method):
    return specialRole(method, 'founder')
  
def super(method):
    return specialRole(method, 'super')  

def specialRole(method, roleName):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    @authenticate
    def wrapper(self, *args, **kwargs):  
        if isinstance(self, SessionRequestHandler) and \
                not set(['super', 'founder', roleName]).intersection(self.identity.roles):  
            
            if isinstance(self, PageRequestHandler) and method.func_name=='get':
                self.gotoLogin()
            elif isinstance(self, JsonRequestHandler):
                self.sendMsg_NoIdentity('非管理员')             
        else: 
            return method(self, *args, **kwargs)

            
    return wrapper  
  


def wrapError(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  
        mr = None
        try:                         
            mr = method(self, *args, **kwargs)
                        
        except StopOnPurpose:
            if not self._finished:
                self.finish()
        except:                  
            if isinstance(self, LogRequestHandler):
                self.log_error(traceback.format_exc())
                                        
            log.error()
            
            try:
                if isinstance(self, PageRequestHandler) and method.func_name=='get':
                    self.gotoError()
                elif isinstance(self, JsonRequestHandler):
                    self.sendMsg_Unknown()
            except StopOnPurpose:
                if not self._finished:
                    self.finish()
                    
        if isinstance(self, LogRequestHandler):
            self.log_flush()
        return mr
            
    return wrapper  


