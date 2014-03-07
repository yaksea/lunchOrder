#encoding=utf-8
'''
Created on 2012-11-19

@author: Administrator
'''
from lunchOrder.controller.handlers.baseRequestHandler import BaseRequestHandler,\
    secure


class Default(BaseRequestHandler):    
    @secure
    def get(self):
        self.render('main.html', ip=self.request.remote_ip)
        

             
     
        
     

        
if __name__ == '__main__':
    pass