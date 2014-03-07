#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
import urllib
import httplib
from lunchOrder.settings import UAP
import json
import traceback
#from lunchOrder.common.auth import apiRequest
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common import log
import urlparse
from lunchOrder.api import apiRequest
from lunchOrder import settings


API_URL = UAP['apiUrl']

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
            
        return apiRequest.request(API_URL, suffix, method, headers, appid=settings.UAP['appId'], **kwargs)  
    
    except ExternalAPIException as ex:
        ex.setType('UAP')
        log.out(ex)
    except:
        log.error()
    
def getUserInfo(userId, sessionId):
    return get('/user/%s' % userId, sessionId)


def check(sessionId):
    data = get('checksession', sid=sessionId)
    if data:
        return data.get('uid')






if __name__ == '__main__':
    url1 = "http://192.168.94.19/uaps"
    url2 = "bbs"
    print urlparse.urljoin(url1, url2)
#    print check('hc6u8fn2v2qu82b3mpuehf68d6')
#    x = urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
#    print x.hostname
#    pass















