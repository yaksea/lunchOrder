#encoding=utf-8
'''
Created on 2013-3-18

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo
import pymongo
from lunchOrder.common import utility
from bson.code import Code
import time
import datetime

def byUsers(dt):
    #独立用户数：2937
    result = mongo.db['log'].group(['identity.uapId'],{'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def byActiveUsers(start, end):
    #当月活跃用户，有编辑数据。
    result = mongo.db['log'].group(['identity.uapId'],{'dateTime':{'$lt':end, '$gt':start}, 'dataId':{'$exists':True}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)

def byHistoryActiveUsers(dt):
    #历史活跃用户，有编辑数据。
    result = mongo.db['log'].group(['identity.uapId'],{'dateTime':{'$lt':dt}, 'dataId':{'$exists':True}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)


    
def byOrganization(dt):
    #独立组织数：418
    result = mongo.db['log'].group(['identity.sysId'],{'identity.sysId':{'$gt':0},'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def byHaveOrgs(dt):
#    有组织的
#    keyf ='''
#                function () {
#                    if(this.identity && this.identity.identities.length>1){
#                        return {uapId:this.identity.uapId};
#                    }
#                    else{
#                        return {uapId:0}
#                    }
#                }
#                '''
    mapper = Code('''
                function () {
                    if(this.identity && this.identity.identities.length>=1 && this.dateTime<%s){
                        emit(this.identity.uapId, 1);
                    }
                }
                '''%dt)
    reducer = Code('''
                function (key, values) {
                    return 1
                }
                ''')
    result = mongo.db['log'].map_reduce(mapper, reducer, 'myresults')    
#    result = mongo.db['log'].group(['identity.uapId'],{'dateTime':{'$lt':dt}}, 
#                                   {'count':0},
#                                   'function(obj, prev) {prev.count++}')    
    return result.find().count()

#def byOnlyPersonal(dt):
#    #只使用个人版(不精确，因为无法排除其后加入组织的用户)：2412
#    #1个组织：561    #2个组织：97    #3个组织：25    #4个组织：9    #5个组织：12    #6个组织：5    #7个组织：4
#    #8个组织：5    #9个组织：4    #10个组织：3    #11个组织：2
#    total = 0
#    for i in range(1, 11):
#        result = mongo.db['log'].group(['identity.uapId'],{'identity.identities':{'$size':i},'dateTime':{'$lt':dt}}, 
#                                       {'count':0},
#                                       'function(obj, prev) {prev.count++}')    
#        total += len(result)
#    return total
#    
def byAndroid(dt):
    #根据来源,android:1515
    result = mongo.db['log'].group(['identity.uapId'],{'mobileInfo.device.platform':{'$in':['android','Android']},'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def byIPhone(dt):
    #根据来源,iphone:1178
    result = mongo.db['log'].group(['identity.uapId'],{'mobileInfo.device.platform':{'$in':['iPhone OS']},'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def byIPhoneJailBreak(dt):
    #根据来源,iphone:1032
    result = mongo.db['log'].group(['identity.uapId'],{'mobileInfo.device.tags':'JailBreak','dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def byWeb(dt):
    #根据来源,web:530
    result = mongo.db['log'].group(['identity.uapId'],{'mobileInfo':{'$exists':False},'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)

def byWebOa(dt):
    #根据来源,web:530
    result = mongo.db['log'].group(['identity.uapId'],{'isEmbeded':True,'dateTime':{'$lt':dt}}, 
                                   {'count':0},
                                   'function(obj, prev) {prev.count++}')    
    return len(result)
    
def theMostEarly():
    #数据统计起点,2013-01-31 20:29:49, 结束：2013-03-18 19:29:17
    result = mongo.db['log'].find({},{'dateTime':1}).sort([('dateTime',pymongo.DESCENDING)])    
    print utility.getFormattedTime(result[0]['dateTime'])
    






if __name__ == '__main__':
    dt = time.mktime(datetime.date(2013,5,1).timetuple())
    print dt
#    print byHaveOrgs(dt)
#    print byOnlyPersonal(dt)
    
    
    