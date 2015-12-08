#encoding=utf-8
'''
Created on 2012-2-9

@author: Administrator
'''
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common import log
from lunchOrder.api import apiRequest
import json


class Requester():
    def __init__(self):
        pass
    
    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)
        
    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)
    
            
    def request(self, method, suffix, **kwargs):
        try:
            return apiRequest.request('https://graph.qq.com', suffix, method, **kwargs)  
        
        except ExternalAPIException as ex:
            ex.setType('QQ API', suffix, **kwargs)
            log.out(ex)
        except:
            log.error()
                    
    
    def check(self, sid):
        ret = self.get("/oauth2.0/me", returnType='str', access_token=sid)
        if ret:
            ret = json.loads(ret[9:-3])
            return ret.get('openid')
    
    
    def getInfo(self, openId, sessionId):    
        ret = self.get("/user/get_user_info", jsonCode='', access_token=sessionId, oauth_consumer_key='101138732', openid=openId)
        if ret['ret'] == 0:
            return ret
 

if __name__ == '__main__':
#     ret = '''callback( {"client_id":"101138732","openid":"5C6F69C8E7F67F1C829BAB58EF9BB835"} );'''
#     print ret[9:-2]
#     ret = json.loads(ret)
# #     ret = json.loads(ret[9:-2])
#     print ret 
#     print Requester().check('0BAE5565E393959199039DB4D0829E3E')
    print Requester().getInfo('5C6F69C8E7F67F1C829BAB58EF9BB835','0BAE5565E393959199039DB4D0829E3E')['nickname']
    
#     print login(515253, 'abcd1234')
#    for x in getSignature('jnu5q8uhdlerg3mhoi4dlim8s6'):
#        print x['_id'], x['signature']
#    for u in getFriendList('sgja79oli9q0cvephj5tfmcuc6')['data']:
#        print u['tagname'], u['tagid']
#    print check('5rv96p8bfh7gudvj6fvpiroim4')
#    print u'"\u9a8c\u8bc1\u8fc7\u671f"'
#    for f in getFriends('sgja79oli9q0cvephj5tfmcuc6'):
#        print f['_id'], f['name']


