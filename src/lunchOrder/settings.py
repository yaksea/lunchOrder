'''
Created on 2012-2-8

@author: Administrator
'''
import os,sys
from lunchOrder.common.tnd import uiModules


ENVIRONMENT = {
               'env':'pro',
               'production' : True,
               'test' : False,
               'dev' : False               
               }


APP = {
            'host': 'http://lunchOrder.91.com'
       }


EMAIL = {
            'host': 'smtp.17j38.com',
            'user' : 'admin@17j38.com',
            'password':'a6l$eX1IJ38'

       }


SESSION = {  
    'cookie_name': 'session_id',
    'cookie_domain': None,
    'cookie_expires': 86400, #24 * 60 * 60, # 24 hours in seconds  
    'ignore_expiry': True,
    'ignore_change_ip': True,
    'expired_message': 'Session expired',
    'httponly': True  
}

CACHE = {
                  'unit_expires': 0,
                  'session_expires': 60 * 60, #20 minutes
#                  '_expires': 20 * 60, #20 minutes
                  'clients' : ['203.195.205.213:11211'],
                  }


PATH = {
        'root' : os.path.dirname(__file__),
        'upload' : os.path.join(os.path.dirname(__file__), "static/upload").replace('\\', '/'),
        'handlers' : os.path.join(os.path.dirname(__file__), "handlers").replace('\\', '/'),
        'log_path': os.path.dirname(__file__),
        "temp_file_path": os.path.join(os.path.dirname(__file__), "temp").replace('\\', '/'),
        }


DB = {
        'host' : '203.195.205.213',
#         'host' : '182.254.211.11',
        'port': 27017,
        'db_name' : 'lunchOrder_pro',
        'user_name' : 'alex',
        'passwords' : 'alkdjiueaj',
        'admin_account': True
      }

REDIS = {
         'host': '203.195.205.213',
         'port':6379,
         'password':'$DSF&%bfg%23',
         'db':1
         }

TND = {
    "ui_modules": uiModules,       
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="

}

  
