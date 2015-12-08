#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
import time
from lunchOrder.common import utility
from lunchOrder.data.mongodbManager import mongo, notDeleted
import pymongo
from lunchOrder.base.wrapper import authenticate, admin

class Default(JsonRequestHandler):
    @authenticate    
    def get(self):
        self.sendMsg()
        


if __name__ == '__main__':
    pass