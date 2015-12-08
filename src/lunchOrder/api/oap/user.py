'''

@author: Administrator
'''
from lunchOrder.api.oap import settings
from lunchOrder.auth import api
from lunchOrder.api.oap.oapClient import OAP_Client
from lunchOrder.data.mongodbManager import mongoHelper
from lunchOrder.common import utility

class User(api.User):
    def __init__(self, env, site):
        self.site = site
        self.setting = setting = settings.__dict__[env].__dict__[site]
        self.handler = OAP_Client(setting.client)
        
    def check(self, sid):
        ret = self.handler.check(sid)
        if ret:
            return '%s_%s'%(self.site, ret['uid'])
    
    
    def login(self, userName, passwords):
        ret = self.handler.login(userName, passwords)
        if ret:
            return dict(sessionId=ret['uap_sid'], 
                        userId='%s_%s'%(self.site, ret['uap_uid']))
            
    def getInfo(self, userId, sid):
        uid = utility.tryParse(userId.split('_')[1], int)
        if uid:
            ret = self.handler.getInfo(uid, sid)
            
            if ret:
                return dict(realName=ret['username'],userId=userId, userName=ret['workid'], site=self.site)
        
    
class User_nd(User):
    def __init__(self, env):
        super(User_nd, self).__init__(env, 'nd')
        
    def login(self, userName, passwords):
        ret = self.handler.post("/passport/login1", account=userName, password=passwords, unitcode="nd")  
        if ret:
            
            return dict(sessionId=ret['sid'], 
                        userId='%s_%s'%(self.site, ret['uid']))
                    
class User_yb(User):
    def __init__(self, env):
        super(User_yb, self).__init__(env, 'yb')
        
        
class User_jm(User):
    def __init__(self, env):
        super(User_jm, self).__init__(env, 'jm')
             
        
if __name__ == '__main__':
    User_yb('dev').login('tqnd515253', '1')
#     User_yb('dev').getInfo(userId, sid)