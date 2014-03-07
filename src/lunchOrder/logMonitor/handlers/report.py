#encoding=utf-8
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

class Default(BaseRequestHandler):    
    def get(self):
        self.render('report.html')

class Data(BaseRequestHandler):    
    def get(self):    
        reportType = self.params['type']
        series = []
        rows = mongo.db['log_analysis'].find().sort([("_id", pymongo.ASCENDING)])
        if reportType == 'Users':
#            总用户数，分组织与非组织
            org = {'name':'组织用户', 'data':[]}
            personal = {'name':'纯个人用户', 'data':[]}
            total = {'name':'total', 'data':[],'type':'spline'}
            series = [personal,org, total]
            for row in rows:
                org['data'].append(row['byHaveOrgs'])
                personal['data'].append(row['byUsers']-row['byHaveOrgs'])            
                total['data'].append(row['byUsers'])            
        elif reportType == 'Organization':
#            总组织数，及组织人数
            orgs = {'name':'组织', 'data':[]}
            users = {'name':'组织用户', 'data':[],'type':'spline'}
            series = [orgs, users]
            for row in rows:
                orgs['data'].append(row['byOrganization'])
                users['data'].append(row['byHaveOrgs'])            
        elif reportType == 'ActiveUsers':
#            活跃用户数，当月、新增、留存
            new = {'name':'新增', 'data':[]}
            old = {'name':'留存', 'data':[]}
            curmMonth = {'name':'total', 'data':[],'type':'spline'}
            series = [new, old, curmMonth]
            rows = list(rows)
            for i in range(len(rows)):
                row = rows[i]
                if i==0:
                    new['data'].append(row['byActiveUsers'])
                    old['data'].append(None)    
                else:
                    lastMonth = rows[i-1]
                    new['data'].append(row['byHistoryActiveUsers']-lastMonth['byHistoryActiveUsers'])
                    old['data'].append(row['byActiveUsers']-new['data'][i])    
                            
                curmMonth['data'].append(row['byActiveUsers'])   
                         
        elif reportType == 'Source':
#            总用户数，按来源分，android\iphone\web\oa
            android = {'name':'android', 'data':[],'type':'spline'}
            iphone = {'name':'iphone', 'data':[],'type':'spline'}
            web = {'name':'web', 'data':[],'type':'spline'}
            pureweb = {'name':'pure web', 'data':[]}
            oa = {'name':'云办公桌面', 'data':[]}
            series = [pureweb, oa, web, android, iphone]
            for row in rows:
                android['data'].append(row['byAndroid'])
                iphone['data'].append(row['byIPhone'])            
                web['data'].append(row['byWeb'])            
                pureweb['data'].append(row['byWeb']-row['byWebOa'])            
                oa['data'].append(row['byWebOa'])            
        
        self.sendMsg(series=series)
         
            
        
        

if __name__ == '__main__':
    pass