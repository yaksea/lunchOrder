#encoding=utf-8
'''
Created on 2012-11-19

@author: Administrator
'''
from tornado.web import RequestHandler
from lunchOrder.logMonitor.handlers import allow_ips
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



class Default(BaseRequestHandler):    
    @secure
    def get(self):
        self.render('main.html')
        

            
        
     
        
     

        
if __name__ == '__main__':
    pass