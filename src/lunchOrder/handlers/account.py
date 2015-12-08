#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.data.mongodbManager import mongo, notDeleted
import pymongo
from lunchOrder.common import utility
import time
from lunchOrder.base.wrapper import authenticate
from lunchOrder.common.utility import tryParse

class Default(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('account.html')

        
#余额
class MyBalance(JsonRequestHandler):
    @authenticate
    def get(self):
        user = mongo.userGroup.find_one({'_id':self.identity.id},['balance'])
        self.sendMsg(balance=user['balance'])
        
#余额
class GroupBalance(JsonRequestHandler):
    @authenticate
    def get(self):
        group = mongo.group.find_one({'_id':self.identity.groupId },['balance'])
        self.sendMsg(balance=-group['balance'])

        
#明细列表
class DetailList(JsonRequestHandler):
    @authenticate
    def get(self):
        group = self.params['group']
        if group:
            
            group = mongo.group.find_one({'_id':self.identity.groupId}, ['balance'])
            
            log = mongo.db['accountLog'].find({'group._id':self.identity.groupId,'isDeleted':notDeleted}).sort([('timestamp', pymongo.DESCENDING)])
            rows = []        
            for l in log: #必有一条
                row = utility.subDict(l, ['type','amount','description','dateTime'])
                row['balance'] = l['group']['balance']
                rows.append(row)
            
            self.sendMsg(rows=rows, remarkName='群组现金账户', balance=group['balance'])
        else:
            id = self.params['id'] or self.identity.id
                
            user = mongo.userGroup.find_one({'_id':id, 'groupId':self.identity.groupId, 
                                             'isDeleted':notDeleted}, ['realName','remarkName', 'balance'])
            
            if not user:
                self.sendMsg_WrongParameter()
            
            log = mongo.db['accountLog'].find({'user._id':id,'isDeleted':notDeleted}).sort([('timestamp', pymongo.DESCENDING)])
            rows = []        
            for l in log: #必有一条
                row = utility.subDict(l, ['type','amount','description','dateTime'])
                row['balance'] = l['user']['balance']
                rows.append(row)
            
            self.sendMsg(rows=rows, remarkName=user.get('remarkName') or user['realName'], balance=user['balance'])
        
#充值
class Recharge(JsonRequestHandler):
    @authenticate
    def post(self):
        amount = utility.tryParse(self.params['amount'], float)
        if not amount or (self.identity.payment['byTurns'] and amount<0):
            self.sendMsg_WrongParameter()
            
        toUser = mongo.userGroup.find_one({'_id':self.params['id']})
        toUser or self.sendMsg_NoData('wrong id')
        
        if toUser['groupId'] != self.identity.groupId:
            self.sendMsg_NoPermission('不同群组间不能相互转账')
            
        if not self.identity.payment['byTurns'] and not self.identity.isAdmin:
            self.sendMsg_NoPermission('你没有转账权限！')
        
        log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'amount':amount,
               'type':1}
        log['dateTime'] = utility.getFormattedTime(log['timestamp'])
        log['user'] = toUser
        mongo.userGroup.update({'_id':self.params['id']},{'$inc':{'balance':amount}})
        log['user']['remarkName'] = log['user'].get('remarkName') or log['user']['realName']
        log['description'] = '%s为您充值'%self.identity.remarkName 
        log['groupId'] = self.identity.groupId

        
        log1 = {'_id':utility.getUUID(), 'timestamp':log['timestamp'], 'amount':-amount,
               'type':-1}
        log1['dateTime'] = log['dateTime']
        if self.identity.payment['byTurns']:
            lusr = mongo.userGroup.find_and_modify({'_id':self.identity.id},{'$inc':{'balance':-amount}})
            lusr['remarkName'] = lusr.get('remarkName') or lusr['realName']
            log1['user'] = lusr
        else:
            log1['group'] = mongo.group.find_and_modify({'_id':self.identity.groupId}, {'$inc':{'balance':-amount}})  
            log1['operator'] = self.identity.toJson()
            
        log1['description'] = '为%s充值'%log['user']['remarkName']
        log1['groupId'] = self.identity.groupId
        
        mongo.db['accountLog'].insert([log,log1])
         
        self.sendMsg()


if __name__ == '__main__':
    pass