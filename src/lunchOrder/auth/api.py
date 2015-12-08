'''

@author: Administrator
'''


class User(object):
    def __init__(self, env):
        '''
        site: from different resource
        env: different environment, dev|pro|test|
        '''
        raise NotImplementedError()
    
    def check(self, sid):
#         return userId or None
        raise NotImplementedError()
    
    def login(self,userName, passwords, longTerm=False):
#         return {'sessionId':'', 'userId':'', 'site':''} or None
        raise NotImplementedError()
    
    def logout(self, sid):
#         return {'sessionId':'', 'userId':'', 'site':''} or None
        raise NotImplementedError()
    
    def getInfo(self, userId, sid): #get user detail info
#         return  {'userId':'', 'realName':''}
        pass
    
    def getIdentities(self, sid):
#         return [{'userId':'', 'realName':'user name', 'sysId':'', 'sysName':''},...]
        pass
    
    def changeIdentity(self, sid, userId):
        #return True if success else False
        pass
    

if __name__ == '__main__':
    pass