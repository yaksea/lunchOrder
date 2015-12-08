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
import time

#首页
class Default(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/default.html')
        
#群管理
class Admin(PageRequestHandler):
    @admin
    def get(self):
        self.render('group/admin.html')
            
class CheckName(JsonRequestHandler):
    def check(self, name):
        name = name.strip()[:10]
        if not name or mongo.group.find_one({'name':name, 'isDeleted':mongo.notDeleted},{}):
            return False
        return name
        
    @authenticate
    def post(self):
        name = self.check(self.params['name'])
        self.sendMsg(success=True if name else False)
    

#编辑组信息
class Create(PageRequestHandler, CheckName):
    @authenticate
    def get(self):
        self.render('group/create.html')
        
    @authenticate
    def post(self):
        group = utility.subDict(self.params, ['name', 'tags', 'address', 'brief', 'payment', 'noAudit'], '')
        for kw in ('name', 'address', 'payment', ):
            if not group.get(kw):
                self.sendMsg_WrongParameter('*为必填字段')
                
        group['name'] = self.check(self.params['name'])
        group['address'] = group['address'][:50]
        group['brief'] = (group.get('brief') or '')[:200]
        if not group['name']:
            self.sendMsg_WrongParameter('该群名称已被注册，请另起。')
            
        
        group['_id'] = gid = utility.getUUID()
        
        remarkName = self.identity.remarkName
        ug = self.identity.toJson()
        ug.update({'_id':utility.getUUID(), 'userName':self.identity.userName, 'type':3,
                   'remarkName':remarkName, "balance" : 0, 'groupId':gid, 'roles':['founder']})
        
        group['founder'] = ug
        group['admins'] = []
        group['users'] = 1
        group['isPublic'] = 1
        group['balance'] = 0
        group['createTimestamp'] = time.time()   
        group['createTime'] = utility.getFormattedTime(group['createTimestamp'])
                
        mongo.db['group'].insert(group)
        mongo.userGroup.insert(ug)
        
        self.identity.setGroup(gid)
        self.saveToSession()
        
        self.sendMsg()
        
#获取详细信息
class Detail(JsonRequestHandler):
    @authenticate
    def get(self):
        group = mongo.group.find_one({'_id':self.params['id'] or self.identity.groupId, 'isDeleted':mongo.notDeleted})
        if group:
            self.sendMsg(**group)
        else:
            self.sendMsg_NoData()
        
        
#编辑组信息
class Edit(CheckName):
    @admin
    def post(self):
        group = utility.subDict(self.params, ['tags', 'address', 'brief', 'noAudit'])
        if self.params['name']:
            group['name'] = self.check(self.params['name'])
            if not group['name']:
                self.sendMsg_Duplicated('该群名称已被注册，请另起。')
        
        gid = self.params['id'] or self.identity.groupId
            
        mongo.db['group'].update({'_id':gid},{'$set':group})
        self.sendMsg()
                

class Enterance(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/enterance.html')
    

class List(JsonRequestHandler):
    @authenticate
    def get(self):   
        rows = list(mongo.group.find({'isDeleted':mongo.notDeleted}).sort([('users',-1)]))     
        self.sendMsg(rows=rows)       
     
class MyGroups(JsonRequestHandler):
    @authenticate
    def get(self):       
        if self.params['cached']:
            self.sendMsg(rows=self.identity.userGroups.values())
        elif self.params['groupDetail']:
            userGroups = list(mongo.userGroup.find({'userId':self.identity.userId, 'type':3, 
                                                    'isDeleted':mongo.notDeleted},['groupId', 'balance'])) 
            if not userGroups:
                self.sendMsg(rows=[])
            bmap = {}
            gids = []
            for ug in userGroups:
                gid = ug['groupId']
                bmap[gid] = ug['balance']
                gids.append(gid)
                
            rows = []
            for group in mongo.group.find({'_id':{'$in':gids}, 'isDeleted':mongo.notDeleted}):
                group['balance'] = bmap.get(group['_id']) or 0
                rows.append(group)
            
            rows.sort(key=lambda g:g['balance'])      
            self.sendMsg(rows=rows)
        else:
            userGroups = list(mongo.userGroup.find({'userId':self.identity.userId, 'type':3, 
                                                    'isDeleted':mongo.notDeleted}).sort([('createTimestamp',1)])) 
            self.sendMsg(rows=userGroups)

class Out(JsonRequestHandler):#退群
    @authenticate
    def post(self):
        gid = self.params['gid']
        ugid = self.params['ugid']
        if gid:
            ug = mongo.userGroup.find_one({'groupId':gid, 'userId':self.identity.userId, 'isDeleted':mongo.notDeleted})
            if ug and ug['balance']==0 and 'founder' not in ug['roles']:
                mongo.userGroup.update({'_id':ug['_id']}, {'$set':{'isDeleted':True}})
                mongo.group.update({'_id':gid},{'$inc':{'users':-1}})
                if gid == self.identity.groupId:
                    self.identity.setGroup()
                else:
                    self.identity.setGroup(self.identity.groupId)
                self.saveToSession()
        elif ugid:
            if self.identity.isAdmin:
                ug = mongo.userGroup.find_one({'_id':ugid, 'isDeleted':mongo.notDeleted})
                gid = ug['groupId']
                if ug and gid == self.identity.groupId and ug['balance']==0:
                    mongo.userGroup.update({'_id':ugid}, {'$set':{'isDeleted':True}})
                    mongo.group.update({'_id':gid},{'$inc':{'users':-1}})
                    
        self.sendMsg()
                    
class Dismiss(JsonRequestHandler):
    def check(self, groupId):
        if mongo.userGroup.find_one({'groupId':groupId,'balance':{'$ne':0}},[]):
            return False
        return True
        
    
    @admin
    def get(self):
        res = self.check(self.identity.groupId)
        self.sendMsg(success=res)
    
    @admin
    def post(self):
        
        groupId = self.identity.groupId
        if 'founder' in self.identity.roles and self.check(groupId):
            mongo.userGroup.update({'groupId':groupId},{'$set':{'isDeleted':True}}) 
            mongo.group.update({'_id':groupId},{'$set':{'isDeleted':True}}) 
            self.identity.setGroup()
            self.saveToSession()
            self.sendMsg()

        self.sendMsg_WrongParameter()
        
         

#准备加入
class Join(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('group/join.html')

#加群申请
class Apply(JsonRequestHandler):
    @authenticate
    def get(self):
        self.render('group/apply.html')
            
    @authenticate
    def post(self):
        groupId = self.params['groupId']
        group = mongo.group.find_one({'_id':groupId, 'isDeleted':mongo.notDeleted},['name', 'admins', 'founder','noAudit'])
        if not group:
            self.sendMsg_WrongParameter()
        
        approvers = [group['founder']['userId']]
        for admin in group['admins']:
            approvers.append(admin['userId'])
        
        if mongo.apply.find_one({'group._id':groupId, 'applicant.userId':self.identity.userId, 'result.approved':0}):
            self.sendMsg_Duplicated('重复申请')
            
        if mongo.userGroup.find_one({'groupId':groupId, 'userId':self.identity.userId, 'isDeleted':mongo.notDeleted}):
            self.sendMsg_Duplicated('您已经是该群成员，无需再申请')
            
        _apply = {'_id': utility.getUUID(), 'applicant':self.identity.toJson(), 'approvers':approvers,
                  'reason':self.params['reason'], 'group':group, 'createTimestamp':time.time()}   
        _apply['createTime'] = utility.getFormattedTime(_apply['createTimestamp'])
             
        if group.get('noAudit'):
            gid = group['_id']
            ug = _apply['applicant']
            ug.update({"_id" : utility.getUUID(), "balance" : 0, "groupId" : gid,
                  "roles" : [],
                  "type" : 3,
                  "remarkName":''
                  })
            mongo.userGroup.insert(ug)
            mongo.group.update({'_id':gid},{'$inc':{'users':1}})
            
            _apply['result'] = { 'approved':1, 'operator': '', 'reply':''}
        
        else:
            _apply['result'] = { 'approved':0, 'operator': '', 'reply':''}
        
        mongo.apply.insert(_apply)
            
        self.sendMsg(status=(group.get('noAudit') or 0))
        
#我的申请
class MyApply(JsonRequestHandler):
    @authenticate
    def get(self):
        applies = mongo.apply.find({'applicant.userId':self.identity.userId}).sort([('createTimestamp',-1)])
        self.sendMsg(rows=list(applies))
        
#我的申请
class MyApproves(JsonRequestHandler):
    @authenticate
    def get(self):
        cond = {'approvers' : self.identity.userId}
        if not self.params['all']: #all groups
            cond['group._id'] = self.params['groupId'] or self.identity.groupId
            
        applies = mongo.apply.find(cond).sort([('createTimestamp',-1)])
        self.sendMsg(rows=list(applies))
        
    
class Audit(JsonRequestHandler):
    @admin
    def post(self):
        applyId = self.params['id']
        status = utility.tryParse(self.params['status'], int)
        reply = self.params['reply']
        _apply = mongo.apply.find_one({'_id':applyId})
        if _apply and self.identity.userId in _apply['approvers'] and _apply['result']['approved']==0:
            gid = _apply['group']['_id']
            if status == 1:
                ug = _apply['applicant']
                ug.update({"_id" : utility.getUUID(), "balance" : 0, "groupId" : gid,
                      "roles" : [],
                      "type" : 3,
                      "remarkName":''
                      })
                mongo.userGroup.insert(ug)
                mongo.group.update({'_id':gid},{'$inc':{'users':1}})
                
            
            _apply = {'result':{ 'approved':status, 'operator': self.identity.toJson(), 'reply':reply}, 
                      'updateTimestamp':time.time()}
            _apply['updateTime'] = utility.getFormattedTime(_apply['updateTimestamp'])
            
            mongo.apply.update({'_id':applyId}, {'$set':_apply})
            self.sendMsg()
        else:
            self.sendMsg_NoPermission()

        
        

if __name__ == '__main__':
    print len('在1')
#    s = ss()
#    s.cc['pp'] = 'wer'
#    print s.cc
#    print s.kk
    pass
    
    
    