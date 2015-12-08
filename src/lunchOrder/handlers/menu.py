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

class Default(PageRequestHandler):
    @authenticate    
    def get(self):
        self.render('manage/menu.html')
        
#列表
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        menus = mongo.db['menu'].find({'groupId':self.identity.groupId, 'isDeleted':notDeleted},{}).sort([('createTimestamp', pymongo.DESCENDING)])
        self.sendMsg(rows=list(menus))

#
class AllList(JsonRequestHandler):
    @authenticate
    def get(self):
        menus = mongo.db['menu'].find({'groupId':{'$ne': self.identity.groupId}, 'isDeleted':notDeleted},
                                        {}).sort([('inherit.children', pymongo.DESCENDING), ('createTimestamp', pymongo.DESCENDING)])
        self.sendMsg(rows=list(menus))   
#新建
class Create(JsonRequestHandler):
    @authenticate
    def post(self):
        id = utility.getUUID()
        menu = {'createTimestamp':time.time(), '_id':id, 'name':self.params['name']}
        menu['groupId'] = self.identity.groupId
        menu['createTime'] = utility.getFormattedTime(menu['createTimestamp'])
        menu['contact'] = {'phone':self.params['phone'], 'address':self.params['address']}
        mongo.db['menu'].insert(menu)
        self.sendMsg(**menu)
        
#复制
class Copy(JsonRequestHandler):
    @authenticate
    def post(self):
        ids = self.params['ids']
        if not ids:
            self.sendMsg_WrongParameter()
        
        menus = []
        dishes = []
        gid = self.identity.groupId
        
        for menu in mongo.menu.find({'_id':{'$in':ids}, 'isDeleted':mongo.notDeleted}):
            menuId = utility.getUUID()
            for dish in mongo.dish.find({'menuId':menu['_id'], 'isDeleted':mongo.notDeleted}):
                dish['_id'] = utility.getUUID()
                dish['menuId'] = menuId
                dish['groupId'] = gid
                dishes.append(dish)
                
            menu['inherit'] = {'parent': menu['_id']}
            menu['_id'] = menuId
            menu['name'] = self.params['name'] or menu['name']
            menu['contact']['phone'] = self.params['phone'] or menu['contact']['phone']
            menu['contact']['address'] = self.params['address'] or menu['contact']['address']
            menu['groupId'] = gid
            menu['createTimestamp'] = time.time()
            menu['createTime'] = utility.getFormattedTime(menu['createTimestamp'])
            menus.append(menu)
        
        if menus:
            mongo.menu.insert(menus)
            mongo.menu.update({'_id':{'$in':ids}},{'$inc':{'inherit.children':1}}, multi=True)
            if dishes:
                mongo.dish.insert(dishes)
                
        self.sendMsg()

        
#编辑
class Edit(JsonRequestHandler):
    @authenticate
    def post(self):
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
    @admin
    def post(self):
        id = self.params['id']        
        mongo.db['menu'].update({'_id':id}, {'$set':{'isDeleted':1}})
        self.sendMsg()



if __name__ == '__main__':
    pass