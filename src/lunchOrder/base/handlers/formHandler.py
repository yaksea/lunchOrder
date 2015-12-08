#encoding=utf-8
'''
Created on 2012-9-24

@author: Administrator
'''

from lunchOrder import settings

import urllib
from lunchOrder.common.exception import StopOnPurpose
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
import re


class FormRequestHandler(JsonRequestHandler):
    def checkByRex(self, val):
        return re.match(r"(\w+)\s", val)

#     def checkByRex(val):
#         return re.match(r"^[a-zA-Z][a-zA-Z0-9_]{5,15}$", val, re.I)





if __name__ == '__main__':
    print checkByRex('asdfss') 

            

            