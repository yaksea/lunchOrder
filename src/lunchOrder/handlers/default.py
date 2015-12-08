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
        groupId = self.params['groupId']
        if groupId:
            force = True if self.params['force'] else False
            if self.identity.setGroup(groupId, force=force):
                self.saveToSession()
#                 self.render('order.html')
                self.redirect('/order')
            else:
                self.render('group/apply.html')
#                 self.redirect('/group/apply?groupId=%s'%groupId)
        else:
            if not self.identity.userGroups:
                self.render('group/join.html')
#                 self.redirect('/group/join')
            else:
#                 self.render('order.html')
                self.redirect('/order')



        




if __name__ == '__main__':
    pass