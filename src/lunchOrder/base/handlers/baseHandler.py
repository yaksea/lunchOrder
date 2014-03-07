#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
import json
from lunchOrder.common.tnd.params import Params
from lunchOrder import settings
from tornado.web import RequestHandler
import zlib
from lunchOrder.common import httpAgentParser


class BaseRequestHandler(RequestHandler): 
    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        self._params = None              
        if self.request.headers.get('Content-Encoding') == 'gzip':
            self.request.body = zlib.compressobj().decompress(self.request.body)

    
    def render(self, *args, **kwargs):
        self.set_header('Cache-Control', 'no-cache')
        super(BaseRequestHandler, self).render(*args, context=self, **kwargs)
        

    @property
    def params(self):
        if not self._params:
            self._params = Params()
            for argName in self.request.arguments:
                args = self.get_arguments(argName)
                if len(args)>1:
                    self._params[argName] = args
                else:
                    self._params[argName] = args[0]
                    
            if self.request.method.upper() == 'POST':
                try:
                    self._params.update(json.loads(self.request.body))
                except:
                    pass
                                
        return self._params 

    


    @property
    def referer(self):
        return self.request.headers.get('Referer') or self.request.uri
    
            
    
    @property
    def clientInfo(self):   
        _info = {'ip':self.request.remote_ip}
        try:
            _browserInfo = httpAgentParser.detect(self.request.headers['user-agent'])
            _info.update(_browserInfo)
        except:
            pass
        return _info;
          

    
        
if __name__ == '__main__':
    print u'\u8be5\u7248\u672c\u4e0d\u652f\u6301\u4e2a\u4eba\u5ba2\u6237\uff0c\u8bf7\u5230 http://lunchOrder.91.com/app \u4e0b\u8f7d\u6700\u65b0\u7248\u672c\u3002'
#    dt = time.time()
#    print dt
#    for i in range(10):
##        print i
#        user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20100101 Firefox/15.0.1'
#        uas = uas_parser.parse(user_agent)
##        print uas['ua_name']
##        print uas['os_name']
#        print uas
#    print time.time()
#    print time.time()-dt
       
       
        