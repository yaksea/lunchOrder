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
from lunchOrder.common.utility import tryParse

class Default(PageRequestHandler):
    @authenticate
    def get(self):
        self.render('order.html')

#创建订单
class Create(JsonRequestHandler):
    @authenticate
    def post(self):
        order = {'_id':utility.getUUID(), 'createTimestamp':time.time(), 'status':0}
        
        order['createTime'] = utility.getFormattedTime(order['createTimestamp'])
        order['name'] = self.params['name']
        order['menuId'] = self.params['menuId']
        order['note'] = self.params['note']
        order['groupId'] = self.identity.groupId
        order['sponsor'] = self.identity.toJson()
        mongo.db['order'].insert(order)
        
        self.sendMsg()
        
        
    
        
#获取当前订单
class AvailableOrders(JsonRequestHandler):
    @authenticate
    def get(self):
        orders = mongo.db['order'].find({'status':0,'groupId':self.identity.groupId},
                        {'name':1, 'note':1, 'createTime':1, 'menuId':1, 
                         'sponsor':1}).sort([('createTimestamp', pymongo.DESCENDING)])
        self.sendMsg(rows=list(orders))
        
        
#选中，点餐
class Book(JsonRequestHandler):
    @authenticate
    def post(self):
        orderId = self.params['orderId']
        dishId = self.params['dishId']
        order = mongo.db['order'].find_one({'_id':orderId},{'status':1, 'name':1, 'sum':1})
        if order['status'] != 0:
            self.sendMsg_NoData()
        
        dish = mongo.db['dish'].find_one({'_id':dishId},{'name':1, 'price':1})
        
        od = mongo.db['orderDetail'].find_one({'order._id':orderId, 'user._id':self.identity.userId})
        if od:
            mongo.db['order'].update({'_id':orderId}, {'$inc':{'sum.amount':-od['dish']['price'], 
                                                               'sum.dishCount.%s'%od['dish']['_id']:-1 }})
            od['dish'] = dish
            od['updateTimestamp'] = time.time()
            od['updateTime'] = utility.getFormattedTime(od['createTimestamp'])            
            mongo.db['orderDetail'].update({'_id':od.pop('_id')},{'$set':od})
        else:
            od = dict(dish=dish, _id=utility.getUUID(), order=order)
            od['user'] = self.identity.toJson()
            od['createTimestamp'] = time.time()
            od['groupId'] = self.identity.groupId
            od['createTime'] = utility.getFormattedTime(od['createTimestamp'])            
            mongo.db['orderDetail'].insert(od)
        
        mongo.db['order'].update({'_id':orderId}, {'$inc':{'sum.amount':od['dish']['price'], 
                                                     'sum.dishCount.%s'%od['dish']['_id']:1 },
                                                       '$addToSet':{'sum.dishes':od['dish']}})
            
        
        self.sendMsg()
            

#获取列表信息
class MyOrderDetail(JsonRequestHandler):
    @authenticate
    def get(self):
        od = mongo.db['orderDetail'].find_one({'order._id':self.params['id'], 'user._id': self.identity.userId},
                                        {'dish':1})
        if od:   
            self.sendMsg(**od)
        else:
            self.sendMsg_NoData()
        

#取消预订
class RecallBook(JsonRequestHandler):
    @authenticate
    def post(self):
        orderId = self.params['id']
        od = mongo.db['orderDetail'].find_one({'order._id':orderId, 'user._id':self.identity.userId})
        if od:
            mongo.db['order'].update({'_id':orderId}, {'$inc':{'sum.amount':-od['dish']['price'], 
                                                               'sum.dishCount.%s'%od['dish']['_id']:-1 }})       
            mongo.db['orderDetail'].remove({'_id':od.pop('_id')})
            
        self.sendMsg()
             
        
        
#获取订单统计信息      
class Sum(JsonRequestHandler):
    @authenticate
    def post(self):
        order = mongo.db['order'].find_one({'_id':self.params['id']},{'name':1,'sum':1,'payer':1,'note':1})        
        self.sendMsg(**order)
        
        
#改变订单状态     
#0：正在点餐中，1：已经订餐，2：已经结单，-1：已取消
class ChangeStatus(JsonRequestHandler):
    @authenticate
    def post(self):
        id = self.params['id']
        order = mongo.db['order'].find_one({'_id':id},{'sponsor':1, 'sum':1 })
        if order['sponsor']['userId']!=self.identity.userId and not self.identity.isAdmin:
            self.sendMsg_NoPermission()
        
        
        status = utility.tryParse(self.params['status'], int)
        if status in (0,1,-1):  #重新启用, 停止点餐, 取消订单
            order = mongo.db['order'].find_and_modify({'_id':id},{'$set':{'status':status}}, new=True)
        elif status == 2: #结单
            
            #改单
            changed_order = {'status':2}
            changed_order['payer'] = {'timestamp':time.time()}
            changed_order['payer']['dateTime'] = utility.getFormattedTime(changed_order['payer']['timestamp']) 
            
            payerId = self.params['payerId']
            if payerId:
                payerId = tryParse(payerId, int)
                changed_order['payer']['user'] = mongo.db['user'].find_one({'_id':payerId})
            else:
                payerId = self.identity.userId
                changed_order['payer']['user'] = self.identity.toJson()            
                      
            order = mongo.db['order'].find_and_modify({'_id':id},{'$set':changed_order}, new=True)
            
            #无金额就此结束
            if order.has_key('sum') and order['sum'].get('amount'):
                #加payer钱
                log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'amount':order['sum']['amount'],
                       'type':2}
                log['user'] = mongo.db['userGroup'].find_and_modify({'userId':payerId, 'groupId':self.identity.groupId},
                                                                         {'$inc':{'balance':order['sum']['amount']}})
                log['dateTime'] = utility.getFormattedTime(log['timestamp'])
                log['description'] = order['name']
                log['groupId'] = self.identity.groupId
                log['linkedData'] = order
                mongo.db['accountLog'].insert(log)            
                
                #扣吃货钱
                ods = mongo.db['orderDetail'].find({'order._id':id},{'user':1,'order':1,'dish':1})
                logs = []
                for od in ods:                
                    log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'type':-2}
                    log['description'] = '%s--%s'%(od['order']['name'], od['dish']['name'])
                    log['amount'] = -od['dish']['price']
                    log['linkedData'] = od
                    log['groupId'] = self.identity.groupId
                    log['user'] = mongo.db['userGroup'].find_and_modify({'userId':od['user']['userId'], 'groupId':self.identity.groupId},
                                                                             {'$inc':{'balance':log['amount']}})
                    log['dateTime'] = utility.getFormattedTime(log['timestamp'])
                    logs.append(log)
                if logs:
                    mongo.db['accountLog'].insert(logs)            
                             
        self.sendMsg(order=order)

        
#获取列表信息
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        orders = mongo.db['order'].find({'groupId':self.identity.groupId},
                                        {'name':1,'status':1,'createTime':1,'menuId':1,'payer':1,
                                         'sum':1,'sponsor':1}).sort([('createTime', pymongo.DESCENDING)])      
        self.sendMsg(rows=list(orders))
        
#获取列表信息
class Detail(JsonRequestHandler):
    @authenticate
    def get(self):
        ods = mongo.db['orderDetail'].find({'order._id':self.params['id']},
                                        {'user':1,'dish':1}).sort([('createTime', pymongo.ASCENDING)])      
        self.sendMsg(rows=list(ods))
        

        



if __name__ == '__main__':
    pass