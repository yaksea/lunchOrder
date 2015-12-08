#encoding=utf-8
'''
Created on 2013-8-20

@author: Alex
'''
from lunchOrder.base.handlers.pageHandler import PageRequestHandler
from lunchOrder.base.handlers.jsonHandler import JsonRequestHandler
from lunchOrder.base.wrapper import authenticate

class User(PageRequestHandler):
    @authenticate    
    def get(self):
        self.render('manage/user.html')
        
class Finance(PageRequestHandler):
    @authenticate    
    def get(self):
        self.render('manage/finance.html')
        
class OrderList(PageRequestHandler):
    @authenticate    
    def get(self):
        self.render('manage/orderList.html')
        
class Sponsor(PageRequestHandler):
    @authenticate    
    def get(self):
        self.render('manage/sponsor.html')




if __name__ == '__main__':
    pass