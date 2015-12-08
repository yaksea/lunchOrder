#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
from lunchOrder import settings
import json
from redis.client import Redis



class RedisClass():
    def __init__(self):    
        password = settings.REDIS.get('password')
        if password:
            self.handler = Redis(host=settings.REDIS['host'], port=settings.REDIS['port'], db=settings.REDIS['db'],
                                 password=password)
        else:
            self.handler = Redis(host=settings.REDIS['host'], port=settings.REDIS['port'], db=settings.REDIS['db'])
            
        self.sessionDict = RedisKey(self.handler, 'SESSION_TOKEN') 
        self.securityCodeDict = RedisKey(self.handler, 'SECURITY_CODE') 
        self.securityCodeNDDict = RedisKey(self.handler, 'SECURITY_CODE_ND') 
        self.securityCodeRGDict = RedisKey(self.handler, 'SECURITY_CODE_RG') 
        self.loginTryTimes = RedisKey(self.handler, 'WRONG_PWDS') 
        self.resetPasswords = RedisKey(self.handler, 'RESET_PWDS') 
        self.emailQueue = RedisQueue(self.handler, 'EMAILS') 
        
        
class Route():
    def __init__(self, redisHandler, redisType, prefix):
        self.redisType = redisType
        self.redisHandler = redisHandler
        self.prefix = prefix
        self.dict = {}
        
    def __getitem__(self, key):
        #key为category id
        value = self.dict.get(key)
        if not value:
            self.dict[key] = value = self.redisType(self.redisHandler, self.prefix+key)
        
        return value
    
    def destroy(self):
        cursor = 0
        while cursor != '0':
            cursor, keys = self.redisHandler.scan(cursor, self.prefix +"*")
            for key in keys:
                self.redisHandler.delete(key)   
   
    
class RedisKey(object):
    class _Method:
        def __init__(self, invoker, method):  
            self._invoker = invoker  
            self._method = method  
      
        def __call__(self, *args, **kwargs): 
            return self._invoker(self._method, *args, **kwargs)
        
    def __init__(self, redisHandler, prefix=''):    
        self.redis = redisHandler
        self.prefix = prefix
        
    def __getattr__(self, name):
        return RedisKey._Method(self.__invoker, name)
    
    def __invoker(self, method, key, *args, **kwargs): 
        return getattr(self.redis, method)(self.prefix+key, *args, **kwargs)
    

class RedisHash(object):
    def __init__(self, redisHandler, hashName=''):    
        self.redis = redisHandler
        self.hashName = hashName
        
    def __setitem__(self, key, value):
        key = str(key)    
        try:
            value = json.dumps(value)
        except:
            pass
        self.redis.hset(self.hashName, key, value)
        
    def __getitem__(self, key):    
        key = str(key)    
        value =  self.redis.hget(self.hashName, key)
        if value:
            try:
#                print 'hash get:%s'%value
                value = json.loads(value)
            except:
                pass
        return value
        
    def __delitem__(self, key):
        key = str(key)    
        self.redis.hdel(self.hashName, key)
        
    def destroy(self):
        self.redis.delete(self.hashName)
        
    
    
class RedisQueue(object): 
    def __init__(self, redisHandler, queueName=''):    
        self.redis = redisHandler
        self.queueName = queueName
    
    def pop(self, count=1):
        if count==1:
            item = self.redis.lpop(self.queueName)
            try:
                item = json.loads(item)
            except:
                pass
        
            return item
        else:
            items = self.redis.lrange(self.queueName, 0, count-1)
            self.redis.ltrim(self.queueName, count, -1)
            l = []
            try:
                for item in items:
                    l.append(json.loads(item))
            except:
                pass
            return l
        
    def bPop(self):
        item = self.redis.blpop(self.queueName)
        try:
            item = json.loads(item[1])
        except:
            pass
    
        return item
            
    def get(self, start, end):
        items = self.redis.lrange(self.queueName, start, end)
        l = []
        try:
            for item in items:
#                print 'get:%s'%item
                l.append(json.loads(item))
        except:
            pass
        return l        
        
    def getAll(self):
        return self.get(0, self.__len__()-1)
         
    def push(self, item, reverse=False):  
        try:
            item = json.dumps(item)
        except:
            pass
        if reverse:
            self.redis.lpush(self.queueName, item)
        else:        
            self.redis.rpush(self.queueName, item)
        
    def extend(self, items, reverse=False):  
        if not items:
            return
        l = []
        try:
            for item in items:
                l.append(json.dumps(item))
        except:
            pass
        if l:
            if reverse:
                self.redis.lpush(self.queueName, *l)
            else:
                self.redis.rpush(self.queueName, *l)
        
    def isEmpty(self):
        if self.redis.llen(self.queueName):
            return False
        else:
            return True
    
    def __len__(self):
        return self.redis.llen(self.queueName)

    def destroy(self):
        self.redis.delete(self.queueName)        

class RedisHashQueue(RedisQueue):
    def __init__(self, redisHandler, queueName=''):
        self._hqName = queueName
        super(RedisHashQueue, self).__init__(redisHandler, queueName)
    
    def pop(self, key, *args, **kwargs):
        self.queueName = self._hqName + str(key)
        return super(RedisHashQueue, self).pop(*args, **kwargs)
        
    def get(self, key, *args, **kwargs):
        self.queueName = self._hqName + str(key)
        return super(RedisHashQueue, self).get(*args, **kwargs)
    
    def getAll(self, key):
        self.queueName = self._hqName + str(key)
        return self.get(key, 0, self.__len__()-1)
                
    def push(self, key, *args, **kwargs):  
        self.queueName = self._hqName + str(key)
        super(RedisHashQueue, self).push(*args, **kwargs)
        
    def extend(self, key, *args, **kwargs):  
        self.queueName = self._hqName + str(key)
        super(RedisHashQueue, self).extend(*args, **kwargs)
        
    def isEmpty(self, key):
        self.queueName = self._hqName + str(key)
        return super(RedisHashQueue, self).isEmpty()
    
    def len(self, key):
        self.queueName = self._hqName + str(key)
        return super(RedisHashQueue, self).__len__()

    def destroy(self, key=''):
        if key:
            self.queueName = self._hqName + str(key)
            super(RedisHashQueue, self).destroy()
        else:
            cursor = 0
            while cursor != '0':
                cursor, keys = self.redis.scan(cursor, self._hqName+"*")
                for key in keys:
                    self.redis.delete(key)  
            
redisDb = RedisClass()
   
    
if __name__ == '__main__':
    redisDb.sessionDict.set('vvv', 'werwerv')
    print redisDb.sessionDict.get('vvv')
#     redisDb.handler.set('vvv', 'werwerv')
#     print redisDb.handler.get('vvv')
    
    
    
    
    
        
