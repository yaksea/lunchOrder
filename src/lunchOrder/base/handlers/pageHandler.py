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
        self.write('<script>parent.location.href="%s"</script>'%url)
        raise StopOnPurpose
    
    def gotoHome(self):
        self.gotoPage('/')
        
    
    def gotoError(self):
        url = '/prompt?' + urllib.urlencode(dict(statusCode=500))
        self.gotoPage(url)

            
    def gotoLogin(self):
        url = '/user/login' +'?'+ urllib.urlencode(dict(returnUrl=self.referer))
        self.redirect(url)
        raise StopOnPurpose
            

            