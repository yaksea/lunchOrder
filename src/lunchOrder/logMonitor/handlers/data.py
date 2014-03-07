'''
Created on 2012-12-13

@author: Administrator
'''
from tornado.web import RequestHandler
from lunchOrder.logMonitor.handlers import allow_ips, BASE_FIELDS
import commands
from lunchOrder.common.cache.memcachedManager import memcachedClient
from lunchOrder.data.mongodbManager import mongo
import json
import os
from lunchOrder import settings
import traceback
from lunchOrder.logMonitor.handlers.baseRequestHandler import BaseRequestHandler,\
    secure
import datetime
import time
from lunchOrder.common.utility import tryParse
import pymongo

class List(BaseRequestHandler):    
    @secure
    def get(self):
        conditions = {}        
        type = self.params['type']
        startTime = tryParse(self.params['startTime'], int, 7)
        endTime = tryParse(self.params['endTime'], int, 0)
        dataId = self.params['dataId']  
        today = datetime.date.today()
        
        if type:
            conditions['type'] = type
        if startTime>=0:
            startTime = int(time.mktime((today-datetime.timedelta(days=startTime)).timetuple()))
            conditions['dateTime'] = {'$gte':startTime}
        if endTime>=0:
            endTime = int(time.mktime((today-datetime.timedelta(days=endTime)).timetuple()))
            if conditions['dateTime']:
                conditions['dateTime'].update({'$lte':endTime})
            else:
                conditions['dateTime'] = {'$lte':endTime}
        if dataId:
            conditions['dataId'] = dataId
        
        fields = list(BASE_FIELDS)
        fields.extend(('ip','mobileInfo.device.platform'))
        cursor = mongo.db['log'].find(conditions, mongo.getFieldsDict(fields)).\
                    sort([('dateTime', pymongo.DESCENDING)])
        rows = []
        for row in cursor:
            if row.has_key('mobileInfo'):
                row['from'] = row['mobileInfo']['device']['platform'] 
                row.pop('mobileInfo')
            else:
                row['from'] = 'web'            
            
            if row.has_key('ip'):
                row.pop('ip')
            
            rows.append(row)
            
        self.sendMsg(rows=rows) 

class Detail(BaseRequestHandler):    
    @secure
    def get(self):    
        row = mongo.db['log'].find_one({'_id':self.params['id']},
                                       mongo.getFieldsDict(BASE_FIELDS, 0))
        self.sendMsg(row=row) 

if __name__ == '__main__':
    pass