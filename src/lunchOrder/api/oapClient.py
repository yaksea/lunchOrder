#encoding=utf-8
'''
Created on 2012-2-9

@author: Administrator
'''
from lunchOrder.settings import OAP_CLIENT
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common import log
from lunchOrder.api import apiRequest


API_URL = OAP_CLIENT['apiUrl']

def getSessionInfo(sid):
    if sid.find('PHPSESSID')<0:
        return 'PHPSESSID=%s; path=/'%sid
    else:
        return sid
    
def get(*args, **kwargs):
    return request('GET', *args, **kwargs)
    
def post(*args, **kwargs):
    return request('POST', *args, **kwargs)

        
def request(method, suffix, sessionId=None, **kwargs):
    try:
        if sessionId:
            headers = {"Cookie": getSessionInfo(sessionId)}
        else:
            headers = {}
            
        return apiRequest.request(API_URL, suffix, method, headers, **kwargs)  
    
    except ExternalAPIException as ex:
        ex.setType('OAP Client', suffix, headers, **kwargs)
        log.out(ex)
    except:
        log.error()
                

def check(sid):
    return post("/passport/check", uap_sid=sid)


def login(account, passwords):
    return post("/passport/login1", account=account, password=passwords, unitcode="nd")
    

def checkWithAllInfo(sid):
    return post("/passport/check", uap_sid=sid)
    
def getIdentities(sessionInfo):       
    data = get("/user/list", sessionInfo)
    if data:
        return data['bind_users']
    else:
        return []


def getDepartments(sessionInfo, sysId):
    return get("/unit/depts", sessionInfo, unitid=sysId, issub=1)['depts']
    
def getUserList(sessionInfo, sysId):
    userList = []
    remain = 1
    while remain >0 :        
        ret = get("/unit/deptusers", sessionInfo, unitid=sysId, size=100, pos=len(userList))
        userList.extend(ret['users'])
        total = ret['total']
        remain = total - len(userList)
    
    return userList

def getUserInfo(sessionInfo, userId):
    
    return get("/user/info", sessionInfo, uid=userId)
 
def changeIdentity(sessionInfo, userId, sysId):
    return post("/passport/changeuser", sessionInfo, unitid=sysId, uid=userId)

def isAdmin(sessionInfo):
    ret = get("/passport/currentuser", sessionInfo, getadmin=1)
    return ret['isadmin']==1
 
if __name__ == '__main__':
    print login('123486', 'hjc803683')
    print login('900926', 'nd.91.com')
    print login('515253', 'weirh123456')
#    print getUserInfo('ud567uvu9unbbgnish3hcrg227', '515253')['username']


