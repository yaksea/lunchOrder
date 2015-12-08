#encoding=utf-8
'''

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo
from lunchOrder.common import utility

def run():
    mongo.group.update({'_id': 'c97739c0fab711e397cd94de80a9cf1e'}, 
                       {'$set':{'name':'ND厦门吃饭群', 'balance':0, 'payment':{'clear':0, 'byTurns':0}}}, True)
    
# def updateGroup():
#     mongo.group.update({'_id': 'c97739c0fab711e397cd94de80a9cf1e'}, 
#                        {'$set':{'users':'ND厦门吃饭群', 'balance':0, 'payment':{'clear':0, 'byTurns':0}}}, True)

def addAdmin():
    mongo.userGroup.update({"realName" : "魏仁海"}, {'$addToSet':{'roles':'founder'}})
    
def addFounder():
    mongo.userGroup.update({"realName" : "严文星"}, {'$addToSet':{'roles':'founder'}})
    
def addAdminsToGroup():
    mongo.group.update({}, {'$set':{'admins':[], 'users':1, 'isPublic':1}}, multi=True)
    for ug in mongo.userGroup.find({"roles" : 'admin'}):
        if ug['realName'] == "严文星":
            mongo.group.update({'_id':ug['groupId']}, {'$set':{'founder':ug}})
        else:
            mongo.group.update({'_id':ug['groupId']}, {'$addToSet':{'admins':ug}})
            
    for group in mongo.group.find({"isDeleted" : mongo.notDeleted}):
        count = mongo.userGroup.find({"isDeleted" : mongo.notDeleted}).count()
        mongo.group.update({'_id':group['_id']}, {'$set':{'users':count}})
    
    
if __name__ == '__main__':
#     run()
#     addFounder()
    addAdminsToGroup()
    print utility.getUUID()