#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.data.mongodbManager import mongo
import pymongo
from lunchOrder.common import utility
import time
from lunchOrder.base.wrapper import authenticate

class Default(PageRequestHandler):
    @authenticate
    def get(self):
        self.redirect('/order')





if __name__ == '__main__':
    pass