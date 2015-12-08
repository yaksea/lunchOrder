#encoding=utf-8
'''
Created on 2015年2月15日

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def sumUserAccount(ugid):
    sum = {'balance':0}
    for log in mongo.db['accountLog'].find({'user._id':ugid,'isDeleted':mongo.notDeleted}).sort([('timestamp',1)]):#
#         print log['linkedData']['order']['name'], log['amount']
        _type = log['type']
        print log.get('amount')
#         print log
#         print sum['balance']
        mongo.accountLog.update({'_id':log['_id']},{'$set':{'user.balance':sum['balance']}})
        if not sum.has_key(_type):
            sum[_type] = 0
        sum[_type] += log['amount']
        sum['balance'] += log['amount']
    
    print sum
#     return sum
    
def orderDetail(ugid):
    sum = 0
    for log in mongo.orderDetail.find({'user._id':ugid,'isDeleted':mongo.notDeleted}):
        if log['sum'].get('amount'):
            print log['order']['name'],log['sum']['amount']
            sum += log['sum']['amount']
    
    print sum
    
def groupAccount(gid):
    sum = {'balance':0}
    for log in mongo.accountLog.find({'group._id':gid,'isDeleted':mongo.notDeleted}).sort([('timestamp',1)]):
        _type = log['type']
#         print log.get('_id')
#         print log.get('amount')
        print sum['balance']
#         print log['group']['balance']
        mongo.accountLog.update({'_id':log['_id']},{'$set':{'group.balance':sum['balance']}})
        if log.get('amount'):
            if not sum.has_key(_type):
                sum[_type] = 0
#             print log['order']['name'],log['sum']['amount']
#             print log['description'],log['amount']
            sum[_type] += log['amount']
            sum['balance'] += log['amount']
    
    print sum
    
def userAccount(gid):
    sum = {'balance':0}
    ua = {}
    for log in mongo.accountLog.find({'user.groupId':gid,'isDeleted':mongo.notDeleted}):
        _type = log['type']
#         if not ua.has_key(log['user']['_id']):
#             ua[log['user']['_id']] = 0
#         
#         ua[log['user']['_id']] += log['amount']
        
        if log.get('amount'):
            if not sum.has_key(_type):
                sum[_type] = 0
#             print log['order']['name'],log['sum']['amount']
#             print log['_id']#
#             print log['description'],log['amount']
            sum[_type] += log['amount']
            sum['balance'] += log['amount']
    
#     for k,v in ua.items():
#         print k,v    
    print sum
    
def userAccountOrder(gid):
    ua = {}
    for log in mongo.accountLog.find({'user.groupId':gid,'type':-2, 'isDeleted':mongo.notDeleted}).sort([('timestamp',1)]):
        if not ua.has_key(log['description']):
            ua[log['description']] = 0
        
        ua[log['description']] += log['amount']
    
    for k,v in ua.items():
        print k,v  
          
def groupAccountOrder(gid):
    ua = {}
    for log in mongo.accountLog.find({'group._id':gid,'type':2, 'isDeleted':mongo.notDeleted}).sort([('timestamp',1)]):
        if not ua.has_key(log['description']):
            ua[log['description']] = 0
        
        ua[log['description']] += log['amount']
    
    for k,v in ua.items():
        print k,v    
    
def userAccountConflict():
    for log in mongo.accountLog.find():
        if log.get('group') and log['group']['_id']!=log['groupId']:
            print log['_id']
        if log.get('user') and log['user']['groupId']!=log['groupId']:
            print log['_id']
            
#         _type = log['type']
#         if log.get('amount'):
#             if not sum.has_key(_type):
#                 sum[_type] = 0
# #             print log['order']['name'],log['sum']['amount']
#             print log['_id']#log['description'],log['amount']
#             sum[_type] += log['amount']
    

def compare(gid):
    total = 0
    bt = 0
    ss = {}
    ua = {}
    for ug in mongo.userGroup.find({'groupId':gid,'isDeleted':mongo.notDeleted}):# 
        print ug['realName'], ug['balance']
        sum = sumUserAccount(ug['_id'])
        ua[ug['_id']] = sum['balance']
#         print sum
        for _type in sum.keys():
            if not ss.has_key(_type):
                ss[_type] = 0        
            ss[_type] += sum.get(_type,0)
        total += sum['balance']
        bt += ug['balance']
        
    print total,bt
    print ss
#     for k,v in ua.items():
#         print k,v
    
def orderAmount(gid):
    total = 0
    for ug in mongo.order.find({'groupId':gid, 'status':2}).sort([('createTimestamp',1)]):#, 'isDeleted':mongo.notDeleted
        total += ug['sum']['amount']
        print ug['_id']#ug['sum']['amount']
        
    print total


def findGroup():
    for group in mongo.group.find():
        print group['_id'],group['name'],group.get('balance')
        
def updateGroup(gid):
    mongo.group.update({'_id':gid},{'$set':{'balance':-659.13}})
    

    
if __name__ == '__main__':
    ugid = '3578822a108211e4866e00163ee94822'
    gid = "50374566108111e4b97e00163ee94822"
#     updateGroup(gid)
#     findGroup()
    sumUserAccount(ugid)
#     orderDetail(ugid)
#     groupAccount(gid)
#     userAccount(gid)
#     userAccountOrder(gid)
#     groupAccountOrder(gid)
#     orderAmount(gid)
#     compare(gid)
#     userAccountConflict()