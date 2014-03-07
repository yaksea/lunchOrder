#encoding=utf-8
'''
Created on 2013-3-18

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo
import pymongo
from lunchOrder.common import utility
import datetime
import time
from lunchOrder.logMonitor.analysis import series

def runHistory():
    #从2-1到当前下月1号
    for month in range(2,6):
        start = time.mktime(datetime.date(2013,month,1).timetuple())
        end = time.mktime(datetime.date(2013,month+1,1).timetuple())
        label = '2013-%s'%month
        print label
        result = {}
        
        for p in dir(series):
            if p.startswith('by'):
                m = getattr(series, p)
                if p=='byActiveUsers':
                    result[p] = m(start, end)
                else:
                    result[p] = m(end)
                
        print result 
        mongo.db['log_analysis'].update({'_id':label},{'$set':result}, True)
    
    
def runCurrent():
    today = datetime.date.today().timetuple()
    year = today.tm_year
    month = today.tm_mon
    start = time.mktime(datetime.date(year,month,1).timetuple())
    end = time.mktime(datetime.date(year,month+1,1).timetuple())
    label = '%s-%s'%(year,month)
    print label
    result = {}
    
    for p in dir(series):
        if p.startswith('by'):
            m = getattr(series, p)
            if p=='byActiveUsers':
                result[p] = m(start, end)
            else:
                result[p] = m(end)
            
    print result 
    mongo.db['log_analysis'].update({'_id':label},{'$set':result}, True)
    
    
def theMostEarly():
    #数据统计起点,2013-01-31 20:29:49, 结束：2013-03-18 19:29:17
    result = mongo.db['log'].find({},{'dateTime':1}).sort([('dateTime',pymongo.ASCENDING)])    
    print utility.getFormattedTime(result[0]['dateTime'])
    






if __name__ == '__main__':
    runHistory()
    
    
    