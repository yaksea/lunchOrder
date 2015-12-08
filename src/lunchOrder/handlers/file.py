#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate, wrapError, admin
from lunchOrder.common import utility
from lunchOrder.base.identity import Identity
from lunchOrder import auth, settings
from lunchOrder.data.redisManager import redisDb
import json
from PIL import Image,ImageDraw,ImageFont
import random
import math
from lunchOrder.common.securityCode import create_validate_code
from StringIO import StringIO

class SecurityCode(JsonRequestHandler):
    @wrapError 
    def get(self):
        img, strs = create_validate_code()
        self.set_header('Cache-Control', 'no-cache')                 
        self.set_header('Content-Type', 'image/gif')
        
        if self.params['nd']:
            redisDb.securityCodeNDDict.set(self.tsid, strs, 60)
        elif  self.params['rg']:
            redisDb.securityCodeRGDict.set(self.tsid, strs, 60)
        else:
            redisDb.securityCodeDict.set(self.tsid, strs, 60)
            
        out = StringIO()
        img.save(out, "gif")
        self.write(out.getvalue())
        out.close()
        self.flush()
        self.finish() 
        
        

if __name__ == '__main__':
    pass