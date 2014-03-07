#encoding=utf-8
'''
Created on 2012-12-13

@author: Administrator
'''
#restart web app
from lunchOrder.controller.handlers.baseRequestHandler import BaseRequestHandler,\
    secure
import commands
import os
import traceback
import time
import tornado
import datetime
from lunchOrder import settings

class Default(BaseRequestHandler):
    @secure
    def get(self):
        self.render('command.html')    
        
class Restart(BaseRequestHandler):
    @secure    
    def get(self):
        if settings.ENVIRONMENT['test']:
            output =  commands.getoutput('sh restart_test.sh')
#            self.write('test.')   
        else:
#            self.write('pp.')   
            output =  commands.getoutput('sh run.sh')
            
        self.write('done.')   
        
#shell 命令        
class Execute(BaseRequestHandler):
    @secure   
#    @tornado.web.asynchronous  
    def post(self):
#        output = None
#        tryTimes = 0
#        
#        def _callback():
#            if not output:
#                tryTimes += 1
#                tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), _callback)
#                if tryTimes>3:
#                    self.send_error(408)
#                    self.finish()
#                    return
            
            try:
                cmd = self.get_argument('cmd').replace('\r\n', ';')
                output = commands.getoutput(cmd)
                self.sendMsg(output, 200)
            except Exception, ex:
                traceback.print_exc()
                self.sendMsg(traceback.format_exc(), 500)
            
#        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), _callback)
            
        
         
##check memcached alive    
#class CheckCache(BaseRequestHandler):
#    def operate(self):
#        output = commands.getoutput('ps aux|grep memca  ')
#        self.write(output)  


        
if __name__ == '__main__':
    print os.path.abspath(os.curdir)