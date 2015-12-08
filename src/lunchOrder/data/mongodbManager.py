#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
from gridfs import GridFS
from lunchOrder import settings
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient


class GridFSEx(GridFS):   
    def __init__(self, database, collection="fs"):
        super(GridFSEx, self).__init__(database, collection)
        self.files = database[collection].files
        
    def update(self, *args, **kwargs):
        self.files.update(*args, **kwargs)
    
    def remove(self, *args, **kwargs):
        self.files.remove(*args, **kwargs)
        
    def find(self, *args, **kwargs):
        return self.files.find(*args, **kwargs)  
          
    def find_one(self, *args, **kwargs):
        return self.files.find_one(*args, **kwargs)
            
    def findPaging(self, pageSize, *args, **kwargs):
        #必须结合结果记录的修改，否则会死循环
        go = True
        
        fil = self.files
        
        while go == True:
            cursor = fil.find(*args, **kwargs).limit(pageSize)
            i = 0
            for row in cursor:
                i += 1
                yield row
            if i == pageSize:
                go = True
            else:
                go = False    
                    
class CollectionEx(Collection):
    def __init__(self, *args, **kwargs):
        super(CollectionEx, self).__init__(*args, **kwargs)
        
    def batchUpsert(self, ids=[], values={}):
        for _id in ids:
            super(CollectionEx, self).update({'_id':_id}, values, True)

    def findPaging(self, pageSize, *args, **kwargs):
        #必须结合结果记录的修改，否则会死循环
        go = True
        
        while go == True:
            cursor = super(CollectionEx, self).find(*args, **kwargs).limit(pageSize)
            i = 0
            for row in cursor:
                i += 1
                yield row
            if i == pageSize:
                go = True
            else:
                go = False

            
class mongoHelper():
    
    notDeleted = {'$nin': [True, 1, 2]}
    
    def __init__(self, setting):    
        connection = MongoClient(setting['host'], setting['port'])    
        self.db = connection[setting['db_name']]
        if setting.has_key('user_name') and setting.has_key('passwords'):
            if setting.get('admin_account'):
                connection['admin'].authenticate(setting['user_name'], setting['passwords'])
            else:
                self.db.authenticate(setting['user_name'], setting['passwords'])
        
        self.fs = GridFSEx(self.db)
        self.prefix = setting.get('prefix') or ''  #collection prefix

    def __getattr__(self, name):
        if name:
            return CollectionEx(self.db, self.prefix+name)
    
        

        
mongo = mongoHelper(settings.DB)

notDeleted = {'$nin': [True, 1, 2]}        
    
if __name__ == '__main__':
    for row in mongo.voter.findPaging(100,{'dirty':{'$exists':False}}):
        mongo.voter.update({'_id':row['_id']},{'$set':{'dirty':1}})
#         print type(row)
    print 'done.'
    
    
    
    
    
    
        
