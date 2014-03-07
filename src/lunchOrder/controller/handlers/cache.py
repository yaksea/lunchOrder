'''
Created on 2012-12-13

@author: Administrator
'''
#    clean cache
from lunchOrder.common.cache.memcachedManager import memcachedClient
from lunchOrder.controller.handlers.baseRequestHandler import BaseRequestHandler,\
    secure
    
class Clean(BaseRequestHandler):
    @secure    
    def get(self):
        memcachedClient.conn.flush_all();
        self.write('done.') 
        
    
#test memcached
class Check(BaseRequestHandler):
    @secure
    def get(self):
        memcachedClient.set('memcached is alive', 10000, 'asdfqwerasdf')
        value = memcachedClient.get('asdfqwerasdf')
        if value == 'memcached is alive':
            self.write(value)
        else:
            self.write('memcached is not alive')
            
        
        
if __name__ == '__main__':
    pass