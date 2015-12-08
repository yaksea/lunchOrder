'''

@author: Administrator
'''
from lunchOrder.auth import api
from lunchOrder.common import utility
from lunchOrder.api.qq.requester import Requester
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.data.redisManager import redisDb
import json

class User(api.User):
    def __init__(self, env):
        pass
        
    def check(self, sid):
        data = redisDb.sessionDict.get(sid)
        if data:
            data = json.loads(data)
            if not data['longTerm']:
                redisDb.sessionDict.expire(sid, 1800)
                
            return data['userId']

    
    def login(self,userName, passwords, longTerm):
#         return {'sessionId':'', 'userId':'', 'site':''} or None
        user = mongo.user.find_one({'userName':userName, 'passwords':passwords, 'site':'pri', 'isDeleted':mongo.notDeleted})
        if user:
            sid = utility.getUUID()
            if longTerm:
                expired = 3600*24*30
            else:
                expired = 1800
            
            data = dict(userId=user['_id'], longTerm=longTerm)
            redisDb.sessionDict.set(sid, json.dumps(data), expired)
            return dict(sessionId=sid, userId=user['_id'], site='pri')
    
    def logout(self, sid):
        redisDb.sessionDict.delete(sid)
        
if __name__ == '__main__':
#     User_yb('dev').login('tqnd515253', '1')
#     User_yb('dev').getInfo(userId, sid)
    pass