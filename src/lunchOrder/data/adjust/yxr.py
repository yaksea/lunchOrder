#encoding=utf-8
'''
Created on 2015年2月25日

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def run1():
    for al in mongo.accountLog.find({"dateTime" : "2015-01-29 20:35:51"}):
        if al.has_key('user'):
            mongo.userGroup.update({'_id':al['user']['_id']},{'$inc':{'balance':-al['amount']}})
        if al.has_key('group'):
            mongo.group.update({'_id':al['group']['_id']},{'$inc':{'balance':-al['amount']}})
            
    mongo.accountLog.update({"dateTime" : "2015-01-29 20:35:51"},{'$set':{'isDeleted':True}}, multi=True)
        
        
if __name__ == '__main__':
    run1()