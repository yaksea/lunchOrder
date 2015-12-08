'''

@author: Administrator
'''
from lunchOrder.auth import api
from lunchOrder.common import utility
from lunchOrder.api.qq.requester import Requester

class User(api.User):
    def __init__(self, env):
        self.handler = Requester()
    
    def check(self, sid):
        openId = self.handler.check(sid)
        if openId:
            return 'qq_%s'%openId
    
            
    def getInfo(self, userId, sid):
        openId = userId.split('_')[1]
        if openId:
            ret = self.handler.getInfo(openId, sid)
            
            if ret:
                return dict(realName=ret['nickname'], userId=userId, userName=ret['nickname'], site='qq')
        
    
if __name__ == '__main__':
#     User_yb('dev').login('tqnd515253', '1')
#     User_yb('dev').getInfo(userId, sid)
    pass