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
        orderType = utility.tryParse(self.params['orderType'], int, 1)
        if orderType==1:
            order['menuId'] = self.params['menuId']
        order['orderType'] = orderType
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
                        ['name', 'note', 'createTime', 'menuId', 'orderType', 
                         'sponsor']).sort([('createTimestamp', pymongo.DESCENDING)])
        self.sendMsg(rows=list(orders))
        
        
#选中，点餐，改选菜品
class Book(JsonRequestHandler):
    @authenticate
    def post(self):
#         params = {dishCount:{'dishId':4, 'dishId':4}, orderId:'ddd'}
#         params = {count:4, orderId:'ddd'}
        orderId = self.params['orderId']
        order = mongo.db['order'].find_one({'_id':orderId},['status', 'name', 'sum','orderType'])
        if order['status'] != 0:
            self.sendMsg_NoData()
        
        
        od = mongo.db['orderDetail'].find_one({'order._id':orderId, 'user._id':self.identity.id, 'isDeleted':mongo.notDeleted})
        
        if od: #改订单
            od['updateTimestamp'] = time.time()
            od['updateTime'] = utility.getFormattedTime(od['createTimestamp'])            
        else: ##新增订单
            od = dict(_id=utility.getUUID(), order=order)
            od['user'] = self.identity.toJson()
            od['createTimestamp'] = time.time()
            od['groupId'] = self.identity.groupId
            od['createTime'] = utility.getFormattedTime(od['createTimestamp'])   
                  
        if order['orderType'] == 1:#快餐
            od_dc_new = self.params['dishCount']
            
            
            if od_dc_new:
                dishes = {}
                
                for dish in mongo.db['dish'].find({'_id':{'$in':od_dc_new.keys()}},['name','price']):
                    dishes[dish['_id']] = dish
                    
                od['sum'] = {'dishes':{}, 'count':0, 'amount':0}
                count = 0
                amount = 0
                for dishId, c in od_dc_new.items():
                    dish = dishes[dishId]
    
                    od['sum']['dishes'][dishId] = {'count':c}
                    od['sum']['dishes'][dishId].update(dish)
                    
                    count += c
                    amount += dish['price']*c
                        
                od['sum']['count'] = count
                od['sum']['amount'] = amount
            else: #取消订单
                od['isDeleted'] = True
            
        else:#小炒AA
            count_new = utility.tryParse(self.params['count'], int, 0)
            
            if count_new: 
                od['sum'] = {'count':count_new} 
            else:#取消订单            
                od['isDeleted'] = True
            
                
        mongo.db['orderDetail'].update({'_id':od.pop('_id')},{'$set':od}, True)
        
        or_sum = {'amount':0,'count':0,'dishes':{}}
        
        for od in mongo.db['orderDetail'].find({'order._id':orderId, 'isDeleted':mongo.notDeleted}):
            or_sum['count'] += od['sum']['count']
            or_sum['amount'] += od['sum'].get('amount', 0)  
            od_dishes = od['sum'].get('dishes')
            if od_dishes:
                for did, dish in od_dishes.items():
                    if not or_sum['dishes'].has_key(did):
                        or_sum['dishes'][did] = dish
                    else:
                        or_sum['dishes'][did]['count'] += dish['count']
                             
        mongo.db['order'].update({'_id':orderId}, {'$set':{'sum':or_sum}})
            
        self.sendMsg(**od)
            

#获取列表信息
class MyOrderDetails(JsonRequestHandler):
    @authenticate
    def post(self):
        ods = mongo.db['orderDetail'].find({'order._id':{'$in':self.params['ids']}, 
                                            'user._id': self.identity.id, 'isDeleted':mongo.notDeleted},
                                        ['sum','order'])
        details = {}
        for od in ods:
            details[od['order']['_id']] = od
        self.sendMsg(details=details)
        

        
#获取订单统计信息      
class Sum(JsonRequestHandler):
    @authenticate
    def post(self):
        order = mongo.db['order'].find_one({'_id':self.params['id']},{'name':1,'sum':1,'payer':1,'note':1})        
        self.sendMsg(**order)
        
        
#改变订单状态     
#0：正在点餐中，1：停止点餐，2：已经结单，-1：已取消
class ChangeStatus(JsonRequestHandler):
    @authenticate
    def post(self):
        id = self.params['id']
        order = mongo.db['order'].find_one({'_id':id},['sponsor', 'sum', 'status', 'orderType', 'name'])
        if order['status'] == 2:
            self.sendMsg_Duplicated('不可重复结单')
            
            
        if order['sponsor']['_id']!=self.identity._id and not self.identity.isAdmin:
            self.sendMsg_NoPermission()
        
        
        status = utility.tryParse(self.params['status'], int)
        if status in (0,1,-1):  #重新启用, 停止点餐, 取消订单
            order = mongo.db['order'].find_and_modify({'_id':id},{'$set':{'status':status}}, new=True)
        elif status == 2: #结单
            #修改订单记录
            changed_order = {'status':2}
                      
            #扣吃货钱
            ods = list(mongo.db['orderDetail'].find({'order._id':id, 'isDeleted':mongo.notDeleted},
                                                    ['user','order', 'sum']))
            logs = []
            amount = 0
            if order['orderType']==2: #小炒
                amount = utility.tryParse(self.params['sum'], float, 0)
                if not amount:
                    self.sendMsg_WrongParameter()                
                count = order['sum'].get('count')
                if not count:
                    self.sendMsg_WrongParameter('无人参与的订单无法结单，您可以取消订单。')
                
                changed_order['sum'] = {'amount':amount, 'count':count}
                partition = round(amount/count, 2)
                for od in ods:                
                    log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'type':-2}
                    log['description'] = od['order']['name']
                    log['amount'] = -round(partition*od['sum']['count'], 2)
                    log['linkedData'] = od
                    log['groupId'] = self.identity.groupId
                    log['user'] = mongo.userGroup.find_and_modify({'_id':od['user']['_id']},
                                                                             {'$inc':{'balance':log['amount']}})
                    log['dateTime'] = utility.getFormattedTime(log['timestamp'])
                    logs.append(log)
            else: #快餐
                if order.has_key('sum') and order['sum'].get('amount'):
                    amount = order['sum']['amount']
                if not amount:
                    self.sendMsg_WrongParameter() 
                    
                for od in ods:                
                    log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'type':-2}
                    log['description'] = od['order']['name']
                    log['amount'] = -od['sum']['amount']
                    log['linkedData'] = od
                    log['groupId'] = self.identity.groupId
                    log['user'] = mongo.userGroup.find_and_modify({'_id':od['user']['_id']},
                                                                             {'$inc':{'balance':log['amount']}})
                    log['dateTime'] = utility.getFormattedTime(log['timestamp'])
                    logs.append(log)
            
            
            #修改订单记录
            changed_order['payer'] = {'timestamp':time.time()}
            changed_order['payer']['dateTime'] = utility.getFormattedTime(changed_order['payer']['timestamp']) 
            
            payerId = self.params['payerId'] or self.identity.id
            
            #加payer钱
            log = {'_id':utility.getUUID(), 'timestamp':time.time(), 'amount':amount, 'type':2}
            if self.identity.payment['byTurns']:
                payer = mongo.userGroup.find_and_modify({'_id':payerId},{'$inc':{'balance':amount}})
                payer['remarkName'] = payer.get('remarkName') or payer['realName']
                changed_order['payer']['user'] = log['user'] = payer
            else:#由系统付钱
                log['group'] = mongo.group.find_and_modify({'_id':self.identity.groupId},
                                                                         {'$inc':{'balance':amount}})
                changed_order['payer']['user'] = self.identity.toJson()
                
            log['dateTime'] = utility.getFormattedTime(log['timestamp'])
            log['description'] = order['name']
            log['groupId'] = self.identity.groupId
            log['linkedData'] = order
            logs.append(log)
            
            #数据库持久化
            if logs:
                mongo.db['accountLog'].insert(logs)   
                order = mongo.db['order'].find_and_modify({'_id':id},{'$set':changed_order}, new=True)

                             
        self.sendMsg(order=order)

        
#获取列表信息
class List(JsonRequestHandler):
    @authenticate
    def get(self):
        orders = mongo.db['order'].find({'groupId':self.identity.groupId},
                                        {'name','status','createTime','menuId','payer',
                                         'sum','sponsor','orderType'}).sort([('createTime', pymongo.DESCENDING)]).limit(20)     
        self.sendMsg(rows=list(orders))
        
#获取列表信息
class Detail(JsonRequestHandler):
    @authenticate
    def get(self):
        ods = mongo.db['orderDetail'].find({'order._id':self.params['id'], 'isDeleted':mongo.notDeleted},
                                        ['user','sum']).sort([('createTime', pymongo.ASCENDING)])      
        self.sendMsg(rows=list(ods))
        

     



if __name__ == '__main__':
    cc = {'x':{'dsaf':[1,2,3],"wqe":[1,2,3,5]}}
    x = cc['x']
    cc['x'] = {}
    for k, v in x.items():
        c = v
        c.pop()
    print x
    print cc