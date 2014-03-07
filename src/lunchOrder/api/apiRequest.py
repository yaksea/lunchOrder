#encoding=utf-8
'''
Created on 2012-9-25

@author: Administrator
'''
import urllib
from urlparse import urlparse
import traceback
import json
import httplib
from lunchOrder.common.exception import ExternalAPIException
from lunchOrder.common.utility import urlJoin

def get(apiUrl, suffix=None, headers={}, **params): 
    return request(apiUrl, suffix, 'GET', headers, **params)

   
def post(apiUrl, suffix=None, headers={}, **params):      
    return request(apiUrl, suffix, 'POST', headers, **params)
    
def request(apiUrl, suffix=None, method='GET', headers={}, **params):      
    if suffix: 
        url = urlJoin(apiUrl, suffix)
    else:
        url = apiUrl
        
    urlParts = urlparse(apiUrl)
    
    host = '%s:%d'%(urlParts.hostname, urlParts.port or 80)

     #连接服务器
    if urlParts.scheme == 'https':
        conn=httplib.HTTPSConnection(host)
    else:
        conn=httplib.HTTPConnection(host)
            
    conn.connect()
    
    if method=='GET':
        if len(params)>0:
            params = '?' + urllib.urlencode(dict(params))
            url += params        
#        print url
        conn.request(method, url, None, headers)
    else:
        conn.request(method, url, json.dumps(params), headers)
        
    res=conn.getresponse()
    if res.status == 200:
        content = res.read()
        conn.close()
        return json.loads(content, 'GB2312')
    elif res.status >= 300 and  res.status < 400: #重定向        
        headers = dict(res.getheaders())
        conn.close()
        if headers.has_key('location'):
            return request(headers['location'])
        else:
            raise ExternalAPIException(res.status, url)            
    else:
        conn.close()
        raise ExternalAPIException(res.status, url)

   
        