#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
import time
from lunchOrder.common import utility
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.wrapper import authenticate

        
#新建
class Create(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()        
        id = utility.getUUID()
        dish = {'createTimestamp':time.time(), '_id':id, 'name':self.params['name']}
        dish['createTime'] = utility.getFormattedTime(dish['createTimestamp'])
        dish['price'] = utility.tryParse(self.params['price'], float)
        dish['menuId'] = self.params['menuId']
        dish['groupId'] = self.identity.groupId
        mongo.db['dish'].insert(dish)
        self.sendMsg(id=id)
        
#编辑
class Edit(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()        
        dish = {'updateTimestamp':time.time(), 'name':self.params['name']}
        dish['updateTime'] = utility.getFormattedTime(dish['updateTimestamp'])
        dish['price'] = utility.tryParse(self.params['price'], float)
        mongo.db['dish'].update({'_id':self.params['id']},{'$set':dish})
        self.sendMsg()
        
class Delete(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()
                    
        id = self.params['id']        
        mongo.db['dish'].remove({'_id':id})
        self.sendMsg()
        


if __name__ == '__main__':
    pass