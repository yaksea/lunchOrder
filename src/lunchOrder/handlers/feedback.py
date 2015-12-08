#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.base.wrapper import authenticate, super, wrapError
from lunchOrder.common import utility
import time
from lunchOrder.data.mongodbManager import mongo

class Default(PageRequestHandler, JsonRequestHandler):
    @wrapError    
    def get(self):
        if self.identity:
            self.render('feedback/default.html')
        else:
            self.render('feedback/anonymous.html')
    
    @wrapError
    def post(self):
        message = self.params['message']
        if not message or len(message)>1000:
            self.sendMsg_WrongParameter()
        
        fb = {'_id': utility.getUUID(), 'createTimestamp': time.time(), 'status':0, 'tags':[]}
        fb['message'] = message
        fb['createTime'] = utility.getFormattedTime(fb['createTimestamp'])
        if self.identity:
            fb['user'] = self.identity.toJson()
        
        mongo.feedback.insert(fb)
        self.sendMsg()
        
        
        
class MyList(JsonRequestHandler):
    @authenticate    
    def get(self):
        rows = mongo.feedback.find({'user.userId': self.identity.userId, 'isDeleted':mongo.notDeleted}).sort([('createTimestamp',-1)])
        self.sendMsg(rows=list(rows))
        
class Admin(PageRequestHandler):
    @super    
    def get(self):
        self.render('feedback/admin.html')
        
        
class AllList(JsonRequestHandler):
    @super    
    def get(self):
        status = utility.tryParse(self.params['status'],int)
        condi = {'isDeleted':mongo.notDeleted}
        if status in (0,1):
            condi['status'] = status
        
        rows = mongo.feedback.find(condi).sort([('createTimestamp',-1)])
        self.sendMsg(rows=list(rows))
        
        
class Reply(JsonRequestHandler):
    @super    
    def post(self):
        reply = {'operator':self.identity.toJson(), 'message':self.params['message'], 'createTimestamp':time.time()}
        reply['createTime'] = utility.getFormattedTime(reply['createTimestamp'])
        
        mongo.feedback.update({'_id':self.params['id']},{'$addToSet':{'reply':reply}, '$set':{'status':1}})
        self.sendMsg()
        
    
class Delete(JsonRequestHandler):
    @super    
    def post(self):
        mongo.feedback.update({'_id':self.params['id']},{'$set':{'isDeleted':True}})
        self.sendMsg()




if __name__ == '__main__':
    pass