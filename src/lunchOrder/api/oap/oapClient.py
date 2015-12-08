#encoding=utf-8
'''
Created on 2012-2-9

@author: Administrator
'''
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common import log
from lunchOrder.api import apiRequest


class OAP_Client():
    def __init__(self, setting):
        self.setting = setting
        
    def getSessionInfo(self, sid):
        if sid.find('PHPSESSID')<0:
            return 'PHPSESSID=%s; path=/'%sid
        else:
            return sid
        
    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)
        
    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)
    
            
    def request(self, method, suffix, sessionId=None, **kwargs):
        try:
            if sessionId:
                headers = {"Cookie": self.getSessionInfo(sessionId)}
            else:
                headers = {}
                
            return apiRequest.request(self.setting['apiUrl'], suffix, method, headers, **kwargs)  
        
        except ExternalAPIException as ex:
            ex.setType('OAP Client', suffix, headers, **kwargs)
            log.out(ex)
        except:
            log.error()
                    
    
    def check(self, sid):
        return self.post("/passport/check", uap_sid=sid)
    
    
    def login(self, account, passwords):
        return self.post("/passport/login", account=account, password=passwords)
        
    
    def getInfo(self, userId, sessionId):    
        return self.get("/user/info", sessionId, uid=userId)
 
    def getIdentities(self, sessionId):       
        data = self.get("/user/list", sessionId)
        if data:
            return data['bind_users']
        else:
            return []    
        
    def changeIdentity(self, sessionId, userId, sysId):
        return self.post("/passport/changeuser", sessionId, unitid=sysId, uid=userId)

if __name__ == '__main__':
    pass
#     print login(515253, 'abcd1234')
#    for x in getSignature('jnu5q8uhdlerg3mhoi4dlim8s6'):
#        print x['_id'], x['signature']
#    for u in getFriendList('sgja79oli9q0cvephj5tfmcuc6')['data']:
#        print u['tagname'], u['tagid']
#     print OAP_Client().check('lbpsdehq12mmsmsa6')
#    print u'"\u9a8c\u8bc1\u8fc7\u671f"'
#    for f in getFriends('sgja79oli9q0cvephj5tfmcuc6'):
#        print f['_id'], f['name']


