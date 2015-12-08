#encoding=utf-8
'''
Created on 2012-9-24

@author: Administrator
'''

from lunchOrder import settings

import urllib
from lunchOrder.common.exception import StopOnPurpose
from lunchOrder.base.handlers.logHandler import LogRequestHandler


class PageRequestHandler(LogRequestHandler):
    def gotoPage(self, url):
        self.redirect(url)
        raise StopOnPurpose
    
    def gotoHome(self):
        self.gotoPage('/')
        
    
    def gotoError(self):
        url = '/prompt?' + urllib.urlencode(dict(statusCode=500))
        self.gotoPage(url)

            
    def gotoLogin(self, returnUrl=None):
        self.clearCookie()
        returnUrl = returnUrl or self.request.uri
        url = '/user/login?'+ urllib.urlencode(dict(returnUrl=returnUrl))
        self.gotoPage(url)

            

            