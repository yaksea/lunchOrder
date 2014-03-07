#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.api import oapClient
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate, wrapError
from lunchOrder.common.utility import tryParse
from lunchOrder.common import utility
from lunchOrder.base.identity import Identity

class Login(PageRequestHandler):
    def get(self):
        self.render('user/login.html')

    def post(self):
        if self.login():
            returnUrl = self.params['returnUrl']
            if returnUrl:
                self.redirect(returnUrl)
            else:
                self.redirect("/")            
        else:
            self.redirect('/user/login?error=1')
            
       
class Logout(PageRequestHandler):
    @authenticate
    def get(self):
        self.clearSession()
        self.clearCookie()
        self.gotoLogin()
       
class CheckUnique(JsonRequestHandler):
    def post(self):
        if self.params['loginName']:
            loginName = self.params['loginName'].lower()
            if mongo.db['user'].find_one({'loginName':loginName}):
                self.sendMsg_Duplicated()
            else:
                self.sendMsg()
        elif self.params['email']:
            email = self.params['email'].lower()
            if mongo.db['user'].find_one({'email':email}):
                self.sendMsg_Duplicated()
            else:
                self.sendMsg() 
        else:
            self.sendMsg_WrongParameter()
    
    
class Register(PageRequestHandler, JsonRequestHandler):
    def get(self):
        self.render('user/register.html')
    
    @wrapError    
    def post(self):
        p = self.params
        for kw in ('email', 'passwords', 'loginName', 'realName'):
            if not p.has_key(kw):
                self.sendMsg_WrongParameter()
            elif kw in ('email', 'loginName'):
                p[kw] = p[kw].lower()
                
        if mongo.db['user'].find_one({'$or': [{'loginName' : p['loginName']}, {'email' : p['email']}]}):
            self.sendMsg_WrongParameter()
                
        user = utility.subDict(p, ['email', 'passwords', 'loginName', 'realName', 'mobile'], '')
        user['_id'] = utility.getUUID()            
        mongo.db['user'].insert(user)
        
        self.sessionId = utility.getUUID()
        self.set_cookie(name='sid', value=self.sessionId, path='/')
        self._identity = Identity(user)                                      
        
        ugid = self.get_cookie('ugid')
        if ugid:                      
            userGroup = self.identity.toJson()
            userGroup['type'] = 3
            ug = mongo.db['userGroup'].findAndModify({'_id':ugid, 'type':1},{'$set':userGroup}, new=True)
            if ug:
                self.identity.groupId = ug['groupId']
                self.identity.role = ug.get('role')
        
        self.saveToSession()        
        self.redirect("/") 

    

    
class ChangeInfo(PageRequestHandler,JsonRequestHandler):
    @authenticate
    def get(self):
        self.render('user/changeInfo.html')
        
    @authenticate
    def post(self):
        p = utility.subDict(self.params, ['email', 'realName', 'mobile'], '')
        if not p.has_key('email') or not p.has_key('loginName'):
            self.sendMsg_WrongParameter()        
        p['email'] = p['email'].lower()
        
        mongo.db['user'].update({'_id':self.identity.userId},{'$set':p})
        mongo.db['userGroup'].update({'userId':self.identity.userId},{'$set':p})
        self.sendMsg()
        
     
    
class ChangePasswords(PageRequestHandler,JsonRequestHandler):
    @authenticate
    def get(self):
        self.render('user/changePasswords.html')
        
    @authenticate
    def post(self):
        p = self.params
        mongo.db['user'].update({'_id':self.identity.userId, 'passwords':p['old']},{'$set':{'passwords':p['new']}})
        self.sendMsg()


          
        

#用户列表        
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        users = mongo.db['user'].find({})
        self.sendMsg(rows=list(users)) 
        
        
class Edit(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()
            
        mongo.db['user'].update({'_id':self.params.pop('_id')},{'$set':self.params}, True)
        self.sendMsg() 
        
        



if __name__ == '__main__':
    pass