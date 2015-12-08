#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.common.utility import EmptyClass
from lunchOrder.common.exception import InvalidSessionId
from lunchOrder import auth
from collections import OrderedDict
from lunchOrder.common import utility

class Identity(EmptyClass):
    def __init__(self, site, sessionId, groupId=None):
        self.userId = None
        self.userName = None
        self.roles = []
        self.globalRoles = []
        self.site = site  
        self.sessionId = sessionId          
        self.realName = None
        self.remarkName = None
        self.id = self._id = self.userGroupId = None
        self.groupName = None
        self.payment = None
        self.groupId = groupId
        self.isAdmin = False   
        self.userGroups = OrderedDict()
                  
        
        userId = auth.factory.User.getApi(site).check(sessionId)
        if userId:           
            self.userId = userId
            self.bindIdentity()
        else:
            raise InvalidSessionId
    
    def bindIdentity(self):
        user = mongo.user.find_one({'_id':self.userId})
        if not user:
            user = auth.factory.User.getApi(self.site).getInfo(self.userId, self.sessionId)
            user['_id'] = user.pop('userId')
            mongo.user.insert(user)
        
        self.userId = user['_id']
        self.remarkName = self.realName = user['realName']
        self.userName = user['userName']
        self.globalRoles = user.get('roles') or []
        self.groupId = self.groupId or user.get('curGroupId')
        
        self.setGroup(self.groupId)
        
        
    def setGroup(self, groupId=None, force=True):
        userGroups = list(mongo.userGroup.find({'userId':self.userId, 'type':3, 'isDeleted':mongo.notDeleted}).sort([('createTimestamp',1)]))
#         if not userGroups:
#             ug = {"_id" : utility.getUUID(), "balance" : 0, "groupId" : "c97739c0fab711e397cd94de80a9cf1e",
#                   "realName" : self.realName,
#                   "roles" : [],
#                   "site" : "nd",
#                   "type" : 3,
#                   "userId" : self.userId,
#                   "userName" : self.userName
#                   }
#             userGroups.append(ug)
#             mongo.userGroup.insert(ug)
            
        self.userGroups = OrderedDict()
        
        for ug in userGroups:
            group = mongo.db['group'].find_one({'_id':ug['groupId'], 'isDeleted':mongo.notDeleted})
            if group:
                self.userGroups[ug['groupId']] = {'groupId':group['_id'], 'userGroupId':ug['_id'], 
                                                  'groupName':group['name'], 'roles':ug.get('roles'),
                                                  'payment':group['payment'], 'remarkName':ug.get('remarkName') or self.realName
                                                  }
        if not self.userGroups:
            return False
        
        if groupId and self.userGroups.has_key(groupId):
            self.groupId = groupId
            mongo.user.update({'_id':self.userId}, {'$set':{'curGroupId':self.groupId}}) 
        elif groupId and force and 'super' in self.globalRoles:
            group = mongo.db['group'].find_one({'_id':groupId, 'isDeleted':mongo.notDeleted})
            if group:
                self.userGroups[groupId] = {'groupId':group['_id'], 'userGroupId':group['founder']['_id'], 
                                          'groupName':group['name'], 'roles':ug.get('roles'),
                                          'payment':group['payment'], 'remarkName':'super'}
                self.groupId = groupId
            else:
                return False
        elif force:
            self.groupId = self.userGroups.keys()[0]
            mongo.user.update({'_id':self.userId}, {'$set':{'curGroupId':self.groupId}}) 
        else:
            return False
        
        curGroup =  self.userGroups[self.groupId]
        
        self.remarkName = curGroup['remarkName']
        self.id = self._id = self.userGroupId = curGroup['userGroupId']
        self.roles = self.globalRoles + (curGroup.get('roles') or [])
        self.groupName = curGroup['groupName']
        self.payment = curGroup['payment']
        
        self.isAdmin = 'admin' in self.roles or 'super' in self.roles or 'founder' in self.roles    
        return True

        
    def toJson(self, full=False):    
        ret =  {'_id':self.userGroupId, 'realName':self.realName, 'userId':self.userId, 'groupId':self.groupId, 'roles':self.roles,
                'remarkName':self.remarkName, 'userName':self.userName, 'site':self.site}
        if full:
            ret.update({'isAdmin': self.isAdmin, 'payment':self.payment, 'groupName':self.groupName})
        return ret
                    


    
    
if __name__ == '__main__':
#     dd = OrderedDict()
#     dd['gdf']= 'gdf'
#     dd['asdf']= 'asdf'
#     dd['bnmb']= 'bnmb'
#     
#     print dd.values()
#     print dd
#     if dd:
#         print 'd'
    a = [1,2,3]
    b = [2,3,4,5]
    c = a+b
    print c
    print a
    print b
