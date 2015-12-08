#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate, wrapError, admin, super
from lunchOrder.common import utility
import time

#首页
class Groups(PageRequestHandler):
    @super
    def get(self):
        self.render('super/groups.html')
        

if __name__ == '__main__':
    print len('在1')
#    s = ss()
#    s.cc['pp'] = 'wer'
#    print s.cc
#    print s.kk
    pass
    
    
    