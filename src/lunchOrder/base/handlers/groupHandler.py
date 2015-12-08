#encoding=utf-8
'''
Created on 2012-9-22

@author: Administrator
'''
import base64

from lunchOrder.data.mongodbManager import mongo
from lunchOrder.base.handlers.sessionHandler import SessionRequestHandler

class GroupRequestHandler(SessionRequestHandler):    
    def __init__(self, *args, **kwargs):
        super(GroupRequestHandler, self).__init__(*args, **kwargs)

    def getAdmins(self, groupId=None, types=['admin','founder']):
        groupId = groupId or self.identity.groupId
        admins = {}
        for admin in mongo.userGroup.find({'groupId':groupId, 'isDeleted':mongo.notDeleted, 'roles':{'$in':types}}):
            admins[admin['userId']] = admin
            
        return admins
        

if __name__ == '__main__':
    pass
     
    