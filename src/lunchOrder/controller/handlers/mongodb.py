#encoding=utf-8
'''
Created on 2012-12-13

@author: Administrator
'''
from lunchOrder.controller.handlers.baseRequestHandler import BaseRequestHandler,\
    secure
import json
import traceback
from lunchOrder.data.mongodbManager import mongo

class Default(BaseRequestHandler):
    @secure    
    def get(self):
        self.render('mongodb.html')    

#数据库操作    
class Execute(BaseRequestHandler):
    @secure
    def post(self):
        try:
            collection = self.get_argument('collection')
            operation = self.get_argument('operation')
            query = self.get_argument('query')
            update = self.get_argument('update')
            if operation == 'find':
                expr = 'mongo.db["%s"].%s(%s).limit(200)' % (collection, operation, query)
            elif operation == 'update':
                expr = 'mongo.db["%s"].%s(%s, %s, multi=True, safe=True)' % (collection, operation, query, update)
            else:
                expr = 'mongo.db["%s"].%s(%s, safe=True)' % (collection, operation, query)
            
            print expr
            result = eval(expr)
            if operation == 'find':
                result = list(result)
                message = []
                for r in result:
                    message.append('%s\r\n'%json.dumps(r))
                message = ''.join(message)
            else:
                message = str(result)

            self.sendMsg(message, 200)
        except Exception, ex:
            traceback.print_exc()
            self.sendMsg(traceback.format_exc(), 500)
                
                
if __name__ == '__main__':
    pass