#encoding=utf-8
'''
Created on 2012-2-15

@author: Administrator
'''
import tornado.web
import urlparse


temp = '<li%s><a href="%s">%s</a></li>'
siteMap = {'pages':{'/order':'点餐','/manage/menu':'发起','/manage/orderlist':'订单',
                    '/manage/finance':'财务','/group/userlist':'饭团管理'},'menu':
           ['/order','/manage/menu','/manage/orderlist','/manage/finance','/group/userlist']}

class TopMenu(tornado.web.UIModule):
    def render(self):
        path = urlparse.urlsplit(self.request.uri).path.lower()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        menu = []
        
        if path in siteMap['menu']:  
            for pk in siteMap['menu']:
                if path==pk:   
                    menu.append(temp%(' class="active"',pk,siteMap['pages'][pk]))
                else:
                    menu.append(temp%('',pk,siteMap['pages'][pk]))
        
        return ''.join(menu)


