#encoding=utf-8
'''
Created on 2012-2-8

@author: Administrator
'''
from lunchOrder.common.exception import  InvalidSessionId
from lunchOrder.common.utility import EmptyClass, tryParse
from lunchOrder.api import uap, oapClient
from lunchOrder.data.mongodbManager import mongo
import time
from lunchOrder.common import utility

class Identity(EmptyClass):
                    
    def __init__(self, user, groupId=None):  
        self.setUser(user)
        self.groupId = groupId
        self.role = None
        self.balance = None
        self.userGroups = {}
        self.setGroup()
    
    def setUser(self, user):
        self.userId = user['_id']
        self.loginName = user['loginName']
        self.realName = user['realName']
        self.email = user['email']
        self.mobile = user['mobile']
        
        
    def setGroup(self):
        userGroups = list(mongo.db['userGroups'].find({'userId':self.userId, 'type':3}))
        
        for ug in userGroups:
            group = mongo.db['groups'].find_one({'_id':ug['groupId']})
            if group:
                self.userGroups[ug['groupId']] = {'groupId':group['_id'], 'balance':ug['balance'], 
                                                  'groupName':group['name'], 'role':ug.get('role')}
            
        if self.groupId and self.userGroups.has_key(self.groupId):
            self.role = self.userGroups[self.groupId].get('role')
            self.balance = self.userGroups[self.groupId]['balance']            
        elif len(userGroups)>0:
            self.groupId = userGroups[0]['groupId']
            self.role = userGroups[0].get('role')
            self.balance = userGroups[0]['balance']
                     

        
    def toJson(self):       
        return {'userId':self.userId, 'realName':self.realName, 'email':self.email, 
                'groupId':self.groupId, 'role':self.role}
                    


    
    
if __name__ == '__main__':
    pass
