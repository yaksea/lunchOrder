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
from lunchOrder.base.wrapper import authenticate

        
#列表
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        menus = mongo.db['menu'].find({'groupId':self.identity.groupId, 'isDeleted':notDeleted},{}).sort([('createTimestamp', pymongo.ASCENDING)])
        self.sendMsg(rows=list(menus))
        
#新建
class Create(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()
            
        id = utility.getUUID()
        menu = {'createTimestamp':time.time(), '_id':id, 'name':self.params['name']}
        menu['groupId'] = self.identity.groupId
        menu['createTime'] = utility.getFormattedTime(menu['createTimestamp'])
        menu['contact'] = {'phone':self.params['phone'], 'address':self.params['address']}
        mongo.db['menu'].insert(menu)
        self.sendMsg(id=id)
        
#编辑
class Edit(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()        
        menu = {'updateTimestamp':time.time(), 'name':self.params['name']}
        menu['updateTime'] = utility.getFormattedTime(menu['updateTimestamp'])
        menu['contact'] = {'phone':self.params['phone'], 'address':self.params['address']}
        mongo.db['menu'].update({'_id':self.params['id']},{'$set':menu})
        self.sendMsg()
        
        
#获取菜单详情
class Detail(JsonRequestHandler):
    @authenticate
    def get(self):
        id = self.params['id']
        menu = mongo.db['menu'].find_one({'_id':id})
        dishes = mongo.db['dish'].find({'menuId':id}, {'name':1,'price':1}).sort([('createTimestamp', pymongo.ASCENDING)])
        self.sendMsg(menu=menu, dishes=list(dishes))
        
#
class Delete(JsonRequestHandler):
    @authenticate
    def post(self):
        if not self.identity.isAdmin:
            self.sendMsg_NoPermission()        
        id = self.params['id']        
        mongo.db['menu'].update({'_id':id}, {'$set':{'isDeleted':1}})
        self.sendMsg()



if __name__ == '__main__':
    pass