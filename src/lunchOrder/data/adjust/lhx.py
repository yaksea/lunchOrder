#encoding=utf-8
'''
Created on 2015年2月25日

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def run1():
    for al in mongo.accountLog.find({'user.realName':'林煌祥'}):
        mongo.accountLog_lhx.insert(al)
        
def run2():
    amount = 0
    count = 0
    for al in mongo.accountLog.find({'user._id' : "0442a7a033d511e49f7700163ee94822"}):
        amount += al['amount']
        count += 1
    print amount, count
    
def run3():
    amount = 0
    count = 0
    for al in mongo.accountLog.find({'user._id' : "e7509530a6b111e4982a525400a939c1"}):
        amount += al['amount']
        count += 1
        print 
    print amount, count
    
def run4():
    mongo.accountLog.update({'user._id' : "0442a7a033d511e49f7700163ee94822"}, 
                            {'$set':{'user._id' : "8a18a5ceab4d11e4ad16525400a939c1"}}, multi=True)
    mongo.userGroup.update({'_id' : "8a18a5ceab4d11e4ad16525400a939c1"},{'$inc':{'balance':-104}})
    
def run5():
    mongo.accountLog.update({'user._id' : "e7509530a6b111e4982a525400a939c1"}, 
                            {'$set':{'user._id' : "8a18a5ceab4d11e4ad16525400a939c1"}}, multi=True)
    mongo.userGroup.update({'_id' : "8a18a5ceab4d11e4ad16525400a939c1"},{'$inc':{'balance':36}})
    
def run6():
    for row in mongo.accountLog.find({'user._id' : "8a18a5ceab4d11e4ad16525400a939c1",'type':1,'amount':{'$lt':0}}):
        print row['dateTime'], row['amount']
        
def run7():
    amount = 0
    for row in mongo.accountLog.find({'user._id' : "8a18a5ceab4d11e4ad16525400a939c1",'type':1,'amount':{'$lt':0}}).skip(2):
#         mongo.userGroup.update({'_id' : "8a18a5ceab4d11e4ad16525400a939c1"},{'$inc':{'balance':-row['amount']}})
#         mongo.group.update({'_id' : row['groupId']},{'$inc':{'balance':row['amount']}})
        
#         print row['groupId']
        amount += row['amount']
#         print row['dateTime'], row['amount']
    print amount
    
def run8():
    for row in mongo.accountLog.find({'user._id' : "8a18a5ceab4d11e4ad16525400a939c1",'type':1,'amount':{'$lt':0}}).skip(2):
#         mongo.accountLog.update({'_id':row['_id']},{'$set':{'isDeleted':True}})
        print mongo.accountLog.update({'dateTime':row['dateTime'], 'type':-1},{'$set':{'isDeleted':True}})
        
def run9():
    for row in mongo.accountLog.find({"dateTime" : "2015-02-03 10:37:12",'type':1}):
        mongo.accountLog.update({'_id':row['_id']},{'$set':{'isDeleted':True}})
        mongo.accountLog.update({'dateTime':row['dateTime'], 'type':-1},{'$set':{'isDeleted':True}})
        mongo.userGroup.update({'_id' : "8a18a5ceab4d11e4ad16525400a939c1"},{'$inc':{'balance':-row['amount']}})
        mongo.group.update({'_id' : row['groupId']},{'$inc':{'balance':row['amount']}})
        print row
        
def run10():
    balance = 0
    for row in mongo.accountLog.find({"user._id": "8a18a5ceab4d11e4ad16525400a939c1", 'isDeleted':mongo.notDeleted}):
        mongo.accountLog.update({'_id':row['_id']},{'$set':{'user.balance':balance}})
        balance += row['amount']
#         mongo.accountLog.update({'_id':row['_id']},{'$set':{'isDeleted':True}})
#         mongo.accountLog.update({'dateTime':row['dateTime'], 'type':-1},{'$set':{'isDeleted':True}})
#         mongo.userGroup.update({'_id' : "8a18a5ceab4d11e4ad16525400a939c1"},{'$inc':{'balance':-row['amount']}})
#         mongo.group.update({'_id' : row['groupId']},{'$inc':{'balance':row['amount']}})
        print row['user']['balance']
    print balance
        
if __name__ == '__main__':
    run10()