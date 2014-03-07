#encoding=utf-8
'''
Created on 2012-9-22

@author: Administrator
'''
from lunchOrder.common.cache.sessionManager import Session
import base64

from lunchOrder import settings
from lunchOrder.common.exception import SysUnInit, InvalidSessionId
from lunchOrder.base.identity import Identity
from lunchOrder.base.handlers.baseHandler import BaseRequestHandler
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.common import utility

class SessionRequestHandler(BaseRequestHandler):    
    def __init__(self, *args, **kwargs):
        super(SessionRequestHandler, self).__init__(*args, **kwargs)
        self._identity = None
        self.sessionId = None
        self._session = None
        self.initializeSession()

    def initializeSession(self):                   
        self.sessionId = self.get_cookie('sid')
        
              
                    
    @property
    def session(self):
        if not self._session:
            try:
                sessionId = self.sessionId
                
                if sessionId:
                    self._session = Session(sessionId)
            except:
                pass
                        
        return self._session

    
    @property
    def identity(self):
        if not self._identity:               
            if not self.sessionId:
                return
            
            self._identity = self.session[Session.Keys.Identity]

            if not self._identity:
                self.clearCookie()
                self.clearSession()
                self.log_sign("InvalidSessionId") 
                return
        
                                 
        return self._identity
    
    def saveToSession(self):
        self.session[Session.Keys.Identity] = self._identity
        
        
    
    def login(self):
        user = mongo.db['user'].find_one({'loginName':self.params['loginName'], 'passwords':self.params['passwords']})
              
        if user:
            self.sessionId = utility.getUUID()
            self._identity = Identity(user, self.get_cookie('gid'))                                      
            self.saveToSession()
            self.log_sign() 
                                
            if self.params['rememberMe']:
                self.set_cookie(name='sid', value=self.sessionId, path='/', expires_days=600)
            else:
                self.set_cookie(name='sid', value=self.sessionId, path='/')
            return True
        else:
            return False
            
    
    def clearCookie(self):
        self.clear_cookie('sid')
#        self.clear_cookie('gid')
    
    def clearSession(self):
        if self.session:
            self.session.clean()

                

if __name__ == '__main__':
#    print u'\u60a8\u7684\u5ba2\u6237\u6709\u53d8\u52a8'
#    print urllib.unquote('c2lkPXVhbXZjZWtnMWh0MHNkNzJkMXAwcWNwbGQzJnVpZD0yMDA1MDc1ODU2JnRpZD0mYmlkPSZleHBpcmU9MA==')
    uapc = 'dWlkPTI1MjA4ODQ0OCZzaWQ9bmFlNHVvZWNwYm5pdmVqcjFmbXVxZWVpazMmdGlkPWVlYjE2NDc5M2FmYTIyZjk2MmYzZTUwZGI1NjhjYzQyJmJpZD0zNjQwZTEwOGQyNGI0YzA4YWY0YmQxOGE3NTdjZDMyOSZleHBpcmU9MTM3Nzc0MDk0OA=='
    uapc = base64.b64decode(uapc)
    print uapc
    print uapc.split('&')[0].split('=')[1]
#    
#    print u'\u8bf7\u68c0\u67e5\u662f\u5426\u6b63\u786e\u9009\u62e9\u76f8\u5173\u8054\u7cfb\u4eba\u3002'

     
    