'''
Created on 2012-2-8

@author: Administrator
'''
import os,sys
from lunchOrder.common.tnd import uiModules

VERSION = {
           'server': '0.1.0',
           'android': {'version':'0.1.0', 'url':'http://lunchOrder.91.com/static/phone/91rm_android_V1_2_3_278781_2.apk'},
           'iphone': {'version':'0.1.000', 'url':'http://lunchOrder.91.com/static/phone/91rm(iPhone)v0.1.000.Beta.278521.ipa'},
           }


ENVIRONMENT = {
               'production' : False,
               'test' : False,
               'dev' : True               
               }


APP = {
            'host': 'http://dev.lunchOrder.91.com'
       }

OAP_CLIENT = {
            'apiUrl': 'http://oapnd.91.com'
            }

INTERNAL_POINTS = {
            'apiUrl': 'http://nderp.91.com/Ajax'
            }

#UAP = {
#            'apiUrl': 'http://192.168.94.19/uaps',
#            'loginUrl':"http://uap19.91.com/uaps/uaplogin/login.php",
#            'registerUrl': "http://uap19.91.com/uaps/uaplogin/register.php",
#            'appId': "32",
#             'apiKey': "972R255eEc083aA56dc0449a21B331e0owiENksI" ,
#             'cookieDomain' : '.91.com'
#            }

UAP = {
            'apiUrl': 'http://uap.91.com',
            'loginUrl':"http://reg.uap.91.com/uaplogin/login.php",
            'registerUrl': "http://reg.uap.91.com/uaplogin/register.php",
            'appId': "56c4c51629",
#            'appId': "101",
#            'appId_new': "56c4c51629",
             'apiKey': "Rxlv66haVpRrJ5eAllZClJvkuxppopoRD1RD1JKl",
             'cookieDomain' : '.91.com'
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
                  'session_expires': 20 * 60, #20 minutes
#                  '_expires': 20 * 60, #20 minutes
                  'clients' : ['192.168.19.185:11211'],
                  }

REDIS = {
         'host': '127.0.0.1',
         'port':6379
         }


PATH = {
        'root' : os.path.dirname(__file__),
        'upload' : os.path.join(os.path.dirname(__file__), "static/upload").replace('\\', '/'),
        'handlers' : os.path.join(os.path.dirname(__file__), "handlers").replace('\\', '/'),
        'log_path': os.path.dirname(__file__),
        "temp_file_path": os.path.join(os.path.dirname(__file__), "temp").replace('\\', '/'),
        }


DB = {
        'host' : '192.168.19.184',
        'port': 27017,
        'db_name' : 'lunchOrder'
      }

TND = {
    "ui_modules": uiModules,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="

}

  
