#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate, wrapError, admin
from lunchOrder.common import utility
from lunchOrder.base.identity import Identity
from lunchOrder import auth, settings
import json
from lunchOrder.data.redisManager import redisDb
from lunchOrder.common.validator import Validator
import hashlib
import time

class Login(PageRequestHandler, JsonRequestHandler):
    def get(self):
        self.render('user/login.html')
            
    @wrapError 
    def post(self):
        userName = self.params['userName'].lower()
        tt_userName = 'pri'+userName
        redisDb.loginTryTimes.delete(tt_userName)
        tryTimes = utility.tryParse(redisDb.loginTryTimes.get(tt_userName), int, 0)
        if tryTimes>=5:
            self.sendMsg_OverLoginTryTimes()
        
#         sc = redisDb.securityCodeDict.get(self.tsid)
#         if not sc:
#             self.sendMsg_ExpiredSecurityCode()
        
#         if sc.lower() != self.params['securityCode'].strip().lower():
#             redisDb.securityCodeDict.delete(self.tsid)
#             self.sendMsg_WrongSecurityCode()
            
        passwords = hashlib.md5(self.params['passwords']).hexdigest()
        longTerm = True if self.params['longTerm'] else False
        user = mongo.user.find_one({'userName':userName, 'passwords':passwords, 'site':'pri', 'isDeleted':mongo.notDeleted})
        if user:
            self.sessionId = sid = utility.getUUID()
            if longTerm:
                expired = 3600*24*30
            else:
                expired = 1800
            
            data = dict(userId=user['_id'], longTerm=longTerm)
            redisDb.sessionDict.set(sid, json.dumps(data), expired)
            
            self.set_cookie(name='sid', value=sid, path='/', domain=settings.SESSION['cookie_domain'], expires_days=600)              
            self.set_cookie(name='site', value='pri', path='/', domain=settings.SESSION['cookie_domain'], expires_days=600)    
            self.sendMsg()
        else:
#             redisDb.securityCodeDict.delete(self.tsid)
            redisDb.loginTryTimes.incr(tt_userName)
            redisDb.loginTryTimes.expire(tt_userName, 3600)
            self.sendMsg_FailToLogin(times=tryTimes+1)
            

class LoginND(PageRequestHandler, JsonRequestHandler):
    def get(self):
        self.render('user/loginND.html')
        
    @wrapError
    def post(self):
        userName = self.params['userName'].lower()
        tt_userName = 'nd'+userName
#         redisDb.loginTryTimes.delete(tt_userName)
        tryTimes = utility.tryParse(redisDb.loginTryTimes.get(tt_userName), int, 0)
        if tryTimes>=5:
            self.sendMsg_OverLoginTryTimes()
        
#         sc = redisDb.securityCodeNDDict.get(self.tsid)
#         if not sc:
#             self.sendMsg_ExpiredSecurityCode()
#             
#         if sc.lower() != self.params['securityCode'].strip().lower():
#             redisDb.securityCodeDict.delete(self.tsid)
#             self.sendMsg_WrongSecurityCode()            
                    
        userApi = auth.factory.User.getApi('nd')
        cr = userApi.login(userName, self.params['passwords'])
        if cr:
            self.sessionId = sid = cr['sessionId']
            self.set_cookie(name='sid', value=sid, path='/', domain=settings.SESSION['cookie_domain'], expires_days=600)    
            self.set_cookie(name='site', value='nd', path='/', domain=settings.SESSION['cookie_domain'], expires_days=600)    
                          
            self.sendMsg()
        else:
#             redisDb.securityCodeNDDict.delete(self.tsid)
            redisDb.loginTryTimes.incr(tt_userName)
            redisDb.loginTryTimes.expire(tt_userName, 3600)
            self.sendMsg_FailToLogin(times=tryTimes+1)
            
       
class Logout(PageRequestHandler):
    @wrapError
    def get(self):
        if self.identity and self.identity.site == 'pri':
            auth.factory.User.getApi(self.site).logout(self.sessionId)
        self.clearSession()
        self.clearCookie()
            
        self.gotoPage('/user/login')
        
       
class CheckUnique(PageRequestHandler, JsonRequestHandler):
    @wrapError 
    def post(self):
        userName = self.params['userName'].lower()
        if mongo.user.find_one({'userName':userName, 'site':'pri', 'isDeleted':mongo.notDeleted},{}):
            self.sendMsg_Duplicated()
        else:
            self.sendMsg()
    
    
class Register(PageRequestHandler, JsonRequestHandler):
    def get(self):
        self.render('user/register.html')
    
    @wrapError    
    def post(self):
        user = utility.subDict(self.params, ['passwords', 'userName', 'realName', 'email', 'address', 'mobile'], '')
        for kw in ('passwords', 'userName', 'realName', 'email'):
            if not user.has_key(kw):
                self.sendMsg_WrongParameter()
            elif kw in ('userName',):
                user[kw] = user[kw].lower()
                
        vali = Validator()
        for kw in ('userName', 'email', 'mobile'):
            if user.get(kw):
                if not getattr(vali, kw)(user[kw]):
                    self.sendMsg_WrongParameter()
                    
        if len(user['passwords'])<6:
            self.sendMsg_WrongParameter()
            
#         sc = redisDb.securityCodeRGDict.get(self.tsid)
#         if not sc:
#             self.sendMsg_ExpiredSecurityCode()
#             
#         if sc.lower() != self.params['securityCode'].strip().lower():
#             redisDb.securityCodeDict.delete(self.tsid)
#             self.sendMsg_WrongSecurityCode()            
                        
        if mongo.user.find_one({'userName':user['userName'], 'site':'pri', 'isDeleted':mongo.notDeleted},{}):
            self.sendMsg_Duplicated()
                
        user['_id'] = utility.getUUID()            
        user['site'] = 'pri'          
        mongo.db['user'].insert(user)
        
        sid = utility.getUUID()
        data = dict(userId=user['_id'], longTerm=False)
        redisDb.sessionDict.set(sid, json.dumps(data), 1800)
                    
        self.sessionId = sid
        self.set_cookie(name='sid', value=sid, path='/', domain=settings.SESSION['cookie_domain'], expires_days=600)
        self._identity = Identity('pri', sid) 
        self.saveToSession()                                     
        self.sendMsg()

    
class Forget(PageRequestHandler,JsonRequestHandler):
    @wrapError
    def get(self):
        self.render('user/forget.html')
        
    @wrapError
    def post(self):
        userName = self.params['userName'].strip()
        email = self.params['email'].strip()
        
        user = mongo.user.find_one({'userName':userName,'email':email, 'site':'pri', 'isDeleted': mongo.notDeleted},['realName'])
        if not user:
            self.sendMsg_NoData('用户名与邮箱不匹配。')
        
        rid = utility.getUUID()  
        redisDb.resetPasswords.set(user['_id'], rid, 3600)
        email = {'to':email, 'subject':'[一起叫餐吧]--密码重置'}
        
        email['content'] = '''<html><body><div style="padding:16px 0px 6px 0px">您好，%s：</div>
                            <div style="padding-left:40px;line-height:28px;"><a href="http://17j38.com/user/resetpasswords?rid=%s&uid=%s">请点此将密码重置为：123456</a></div>
                           <div style="padding-left:40px;line-height:28px;">或直接使用浏览器打开以下地址：http://17j38.com/user/resetpasswords?rid=%s&uid=%s</div>
                           <div style="color:red;padding-left:40px;line-height:28px;">该键接地址仅在1小时内有效，有效期至%s</div>
                           <div style="padding:16px 0px 0px 40px;">感谢您使用 [一起叫餐吧]  http://17j38.com</div>
                                
                        '''%(user['realName'], rid, user['_id'], rid, user['_id'], utility.getFormattedTime(time.time()+30))
        redisDb.emailQueue.push(email)
        
        self.sendMsg()

class ResetPasswords(PageRequestHandler):
    @wrapError
    def get(self):
        rid = self.params['rid']
        userId = self.params['uid']
        if rid and userId:
            if rid == redisDb.resetPasswords.get(userId):
                mongo.user.update({'_id':userId},{'$set':{'passwords':'e10adc3949ba59abbe56e057f20f883e'}})
                self.render('user/resetPasswords.html', invalid=False)
            else:
                self.render('user/resetPasswords.html', invalid=True)
        
        self.render('user/resetPasswords.html', invalid=True)
            
        
class GetInfo(JsonRequestHandler):
    @authenticate
    def get(self):
        user = mongo.user.find_one({'_id':self.identity.userId},['realName', 'email', 'mobile', 'address'])
        self.sendMsg(**user)
            
        
        
class ChangeInfo(PageRequestHandler,JsonRequestHandler):
    @authenticate
    def get(self):
        self.render('user/changeInfo.html')
        
    @authenticate
    def post(self):
        user = utility.subDict(self.params, ('realName', 'email', 'address', 'mobile'), '')
        for kw in ('realName', 'email'):
            if not user.has_key(kw):
                self.sendMsg_WrongParameter()
                
        vali = Validator()
        for kw in ('email', 'mobile'):
            if user.get(kw):
                if not getattr(vali, kw)(user[kw]):
                    self.sendMsg_WrongParameter()
                                          
        mongo.db['user'].update({'_id':self.identity.userId},{'$set':user})
        mongo.userGroup.update({'userId':self.identity.userId},{'$set':user})
        self.sendMsg()
        
     
    
class ChangePasswords(PageRequestHandler,JsonRequestHandler):
    @authenticate
    def get(self):
        self.render('user/changePasswords.html')
        
    @authenticate
    def post(self):
        p = self.params
        res = mongo.db['user'].update({'_id':self.identity.userId, 'passwords':p['old']},
                                {'$set':{'passwords':p['new']}}, safe=True)
        if res.get('n'):
            self.sendMsg()
        else:
            self.sendMsg_FailToLogin()


          
class SwitchGroup(JsonRequestHandler):
    @authenticate
    def post(self):
        self.identity.setGroup(self.params['groupId'])
        self.saveToSession()
        self.sendMsg()         

class MyGroups(PageRequestHandler):
    @authenticate
    def get(self):       
        self.render('user/myGroups.html')
        

#用户列表        
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        users = mongo.userGroup.find({'groupId':self.identity.groupId, 'isDeleted':mongo.notDeleted})
        self.sendMsg(rows=list(users)) 
        
        
class Edit(JsonRequestHandler):
    @admin
    def post(self):
        ss = {}
        ugid = self.params['id']
        ug = mongo.userGroup.find_one({'_id':ugid},['roles', 'remarkName', 'groupId', 'userId', 'realName'])
        if not ug:
            self.sendMsg_WrongParameter()
        
        remarkName = self.params['remarkName'].strip()
        if ug.get('remarkName') != remarkName:
            if remarkName:
                ss['$set'] = {'remarkName': remarkName}
            else:
                ss['$unset'] = {'remarkName': 1}
        
        if self.params['isAdmin'] and 'admin' not in ug['roles']:
            ss['$addToSet'] = {'roles': 'admin'}
            mongo.group.update({'_id': ug['groupId']}, {'$addToSet':{'admins':ug}})
        elif not self.params['isAdmin'] and 'admin' in ug['roles']:
            ss['$pull'] = {'roles': 'admin'}
            mongo.group.update({'_id': ug['groupId']}, {'$pull':{'admins':{'_id':ugid}}})
            
        mongo.db['userGroup'].update({'_id':ugid}, ss)
        self.sendMsg() 
        
        

#设为管理员、转让创建者身份
class SetRole(JsonRequestHandler):        
    @admin
    def post(self):
        role = self.params['role']
        ugid = self.params['id']
        if role in ['admin', '']:
            ug = mongo.userGroup.find_one({'_id':ugid}, ['groupId', 'realName', 'remarkName'])
            if not ug:
                self.sendMsg_WrongParameter()
            if ug['groupId'] != self.identity.groupId:
                self.sendMsg_NoPermission()
                
            if role=='admin':
                ug = mongo.userGroup.update({'_id':ugid},{'$addToSet':{'roles':role}})
                mongo.group.update({'_id':ug['groupId']},{'$addToSet':{'admins':ug}})
            else:
                mongo.userGroup.update({'_id':self.params['id']},{'$pull':{'roles':role}})
                mongo.group.update({'_id':ug['groupId']},{'$pull':{'admins':ug}})


if __name__ == '__main__':
    print hashlib.md5('123456').hexdigest()
#     print utility.getFormattedTime(time.time()+30)