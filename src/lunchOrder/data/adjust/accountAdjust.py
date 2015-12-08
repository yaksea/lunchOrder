#encoding=utf-8
'''
Created on 2015年2月15日

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def run1():
    for row in mongo.accountLog.find({"user": {'$exists':True}}):
        if row.get('user') and row['user']['groupId'] != row['groupId']:
            mongo.accountLog_recharge.insert(row)
            mongo.accountLog_recharge.insert(mongo.accountLog.find_one({'dateTime':row['dateTime'], 'type':-1}))

def run2():
    for row in mongo.accountLog.find({"user": {'$exists':True}}):
        if row.get('user') and row['user']['groupId'] != row['groupId']:
            rightGroupId = row['user']['groupId']
            wrongGroupId = row['groupId']
            
            group = mongo.group.find_and_modify({'_id':rightGroupId},{'$inc':{'balance':-row['amount']}})
            mongo.group.update({'_id':wrongGroupId},{'$inc':{'balance':row['amount']}})
            
            mongo.accountLog.update({'_id':row['_id']},{'$set':{'groupId':rightGroupId}})
            mongo.accountLog.update({'dateTime':row['dateTime'], 'type':-1},{'$set':{'group':group, 'groupId':rightGroupId}})
            print row['amount']

def run3():
    for row in mongo.accountLog.find({"user": {'$exists':True}}):
        if not row.get('user'):
            print row['_id']
            continue

if __name__ == '__main__':
    run2()