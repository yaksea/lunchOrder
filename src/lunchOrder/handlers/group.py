#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.api import oapClient
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate
from lunchOrder.common.utility import tryParse
from lunchOrder.common import utility


#编辑组信息
class Edit(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/edit.html')
        
    @authenticate
    def post(self):
        p = utility.subDict(self.params, ['id', 'name', 'workUnit', 'address', 'phone'])
        for kw in ('name', 'address', 'phone'):
            if not p.has_key(kw):
                self.sendMsg_WrongParameter()
        
        id = p.get['id']
        if id:
            self.params.pop('id')
            mongo.db['group'].update({'_id':id},{'$set':self.params})
        else:
            group = self.params.copy()
            group['_id'] = utility.getUUID()            
            mongo.db['group'].insert(group)
            
            self.identity.groupId = group['_id']
            self.identity.role = 'founder'                        
            userGroup = self.identity.toJson()
            userGroup['_id'] = utility.getUUID()
            mongo.db['userGroup'].insert(userGroup)
            self.saveToSession()
                


class Enterance(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/enterance.html')
    
     
class MyGroups(JsonRequestHandler):
    @authenticate
    def get(self):        
        self.sendMsg(rows=self.identity.userGroups.values()) 
        
class SwitchGroup(JsonRequestHandler):
    @authenticate
    def post(self):
        self.identity.groupId = self.params['groupId']
        self.identity.setGroup()
        self.saveToSession()
        self.sendMsg() 
         
class Invite(JsonRequestHandler):
    @authenticate
    def post(self):
        userGroup = {'email':self.params['email'], 'realName':self.params['realName'], 'type':1}
        userGroup['_id'] = utility.getUUID()
        mongo.db['userGroup'].insert(userGroup)
        self.sendMsg()  
    
class InviteConfirm(PageRequestHandler):
    def get(self):
        ugid = self.params['ugid'] #userGroup id
        gid = self.params['gid'] #userGroup id
        self.set_cookie(name='ugid', value=ugid, path='/', expires_days=600)
        if self.identity:
            self.identity.groupId = gid
            self.saveToSession()
            ug = self.identity.toJson()
            ug['type'] = 3
            ug['balance'] = 0
            mongo.db['userGroup'].update({'userId':self.identity.userId,'groupId':gid, 'type':1}, {'$set':ug})
            self.identity.setGroup()        
            self.render('group/inviteConfirmed.html')
        else:
            self.redirect('/user/register?email='+self.params['email'])

        
class UserList(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/userList.html')
        
class DataList(JsonRequestHandler):
    @authenticate
    def get(self):
        ugs = mongo.db['userGroup'].find({'groupId':self.identity.groupId})
        self.sendMsg(rows=list(ugs))
        
        

#设为管理员、转让创建者身份
class SetRole(PageRequestHandler):        
    @authenticate
    def post(self):
        role = self.params['role']
        
        if role=='admin':
            mongo.db['userGroup'].update({'_id':self.params['id']},{'$set':{'role':role}})
        elif role=='founder':
            mongo.db['userGroup'].update({'_id':self.params['id']},{'$set':{'role':role}})
            mongo.db['userGroup'].update({'userId':self.identity.userId, 'groupId':self.identity.groupId},
                                         {'$set':{'role':'admin'}})
        elif not role:
            mongo.db['userGroup'].update({'_id':self.params['id']},{'$unset':{'role':1}})
            


    
#class ss():
#    def __init__(self):
#        self.kk = {}
#        
#    @property
#    def cc(self):
#        return self.kk      
        

if __name__ == '__main__':
#    s = ss()
#    s.cc['pp'] = 'wer'
#    print s.cc
#    print s.kk
    pass
    
    
    