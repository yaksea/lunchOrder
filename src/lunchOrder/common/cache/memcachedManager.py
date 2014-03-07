'''
Created on 2012-2-8

@author: Administrator
'''
from memcache import Client
from lunchOrder import settings

_localCache = {}
PRODUCT_PREFIX = 'LUNCH_ORDER_'

class MemcachedManager():
    class Prefix():
        Session = 'SESSION'
        SysCache = 'ORDER_SYS_CACHE'

        
        
    def __init__(self):
#        if settings.ENVIRONMENT['dev']:
#            pass
#        else:
        self.conn = Client(settings.CACHE['clients'])
        
    def get(self, *arg):
        if len(arg) ==0:
            return None
        arg = [str(i) for i in arg]
        key = PRODUCT_PREFIX+ '|'.join(arg) 
        try:
#            if settings.ENVIRONMENT['dev']:
#                return _localCache.get(key)
#            else:
                return self.conn.get(key)
#            self.conn.
        except:# Client.MemcachedKeyNoneError:
            return None
        
    def set(self, value, timeout, *arg):
        if len(arg) ==0:
            return None  
        arg = [str(i) for i in arg]
        key = PRODUCT_PREFIX+'|'.join(arg)   
#        if settings.ENVIRONMENT['dev']:
#            _localCache[key] = value 
#        else:          
        self.conn.set(key, value, timeout)

    def delete(self, *arg):
        if len(arg) ==0:
            return None
        arg = [str(i) for i in arg]
        key = PRODUCT_PREFIX+'|'.join(arg) 
        try:
#            if settings.ENVIRONMENT['dev']:
#                if _localCache.has_key(key):
#                    _localCache.pop(key)
#            else:                
                self.conn.delete(key)
        except: # Client.MemcachedKeyNoneError:
            return None

memcachedClient = MemcachedManager()

        
if __name__ == "__main__":
    mm = MemcachedManager()
    mm.set('asdfasdf', 1000000, 'gg')
    print mm.get('gg')
    
#    conn = Client(['192.168.94.25:11211'])
#    print conn.set('gg', 'asdfasdf')
    
    
    
    
    