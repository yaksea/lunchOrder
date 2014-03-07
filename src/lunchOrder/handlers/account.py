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
class Balance(JsonRequestHandler):
    @authenticate
    def get(self):
        user = mongo.db['userGroup'].find_one({'userId':self.identity.userId,'groupId':self.identity.groupId },{'balance':1})
        self.sendMsg(balance=user['balance'])

        
#明细列表
class DetailList(JsonRequestHandler):
    @authenticate
    def get(self):
        if self.params['id']:
            userId = tryParse(self.params['id'],int) 
        else:
            userId = self.identity.userId
            
#        user = mongo.db['userGroup'].find_one({'userId':userId, 'groupId':self.identity.groupId})
        log = mongo.db['accountLog'].find({'user.userId':userId, 'groupId':self.identity.groupId, 
                                           'isDeleted':notDeleted}).sort([('timestamp', pymongo.DESCENDING)])
        rows = []        
        for l in log: #必有一条
            row = utility.subDict(l, ['type','amount','description','dateTime'])
            row['balance'] = l['user']['balance']
            rows.append(row)
            
        self.sendMsg(rows=rows, realName=l.pop('user')['realName'])
        
#充值
class Recharge(JsonRequestHandler):
    @authenticate
    def post(self):
        amount = utility.tryParse(self.params['amount'], float)
        if not amount or amount<0:
            self.sendMsg_WrongParameter()
        
        log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'amount':amount,
               'type':1}
        log['dateTime'] = utility.getFormattedTime(log['timestamp'])
        log['user'] = mongo.db['userGroup'].find_and_modify({'userId':self.params['userId'], 
                                                             'groupId':self.identity.groupId},{'$inc':{'balance':amount}})
        log['description'] = '%s为您充值'%self.identity.realName 
        log['groupId'] = self.identity.groupId

        
        log1 = {'_id':utility.getUUID(), 'timestamp':time.time(), 'amount':-amount,
               'type':-1}
        log1['dateTime'] = utility.getFormattedTime(log1['timestamp'])
        log1['user'] = mongo.db['userGroup'].find_and_modify({'userId':self.identity.userId, 
                                                              'groupId':self.identity.groupId},{'$inc':{'balance':-amount}})
        log1['description'] = '为%s充值'%log['user']['realName']
        log1['groupId'] = self.identity.groupId        
        
        mongo.db['accountLog'].insert([log,log1])
         
        self.sendMsg()



if __name__ == '__main__':
    pass