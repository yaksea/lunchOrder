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
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common import log
import urlparse
from lunchOrder.api import apiRequest
from lunchOrder import settings


API_URL = settings.INTERNAL_POINTS['apiUrl']

    
def get(*args, **kwargs):
    return request('GET', *args, **kwargs)
    
def post(*args, **kwargs):
    return request('POST', *args, **kwargs)

def request(method, suffix, sessionId=None, **kwargs):
    try:            
        return apiRequest.request(API_URL, suffix, method, **kwargs)  
    
    except ExternalAPIException as ex:
        ex.setType('INTERNAL_POINTS')
        log.out(ex)
    except:
        log.error()
    
def getUserInfo(userId, sessionId):
    return get('/user/%s' % userId, sessionId)

#uid     职员编号,工号
#Point 积分分值（输入值为正整数）
#type     类型（0积分增加/1积分扣除）
def addPoints(uid, points):
    data = get('A0_frmAjaxFor91U.aspx', action='AddPoint', uid=uid, Point=points, type=0)
    if data:
        return data


#uid         职员编号,工号
#Money     网龙币币值（输入值为正整数）
#Type        类型（0网龙币增加/1网龙币扣除）
def addMoney(uid, points):
    data = get('A0_frmAjaxFor91U.aspx', action='AddNDMoney', uid=uid, Money=points, type=0)
    if data:
        return data






if __name__ == '__main__':
    print addPoints(515253, 500)
#    print u'ip\u5730\u5740\u672a\u6388\u6743'
#    url1 = "http://192.168.94.19/uaps"
#    url2 = "bbs"
#    print urlparse.urljoin(url1, url2)
#    print check('hc6u8fn2v2qu82b3mpuehf68d6')
#    x = urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
#    print x.hostname
#    pass















