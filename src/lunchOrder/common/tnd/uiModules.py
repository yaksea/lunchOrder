#encoding=utf-8
'''
Created on 2012-2-15

@author: Administrator
'''
import tornado.web
import urlparse


temp = '<li%s><a href="%s">%s</a></li>'
siteMap = {'pages':{'/order':'点餐','/manage/sponsor':'发起','/manage/orderlist':'饭事',
                    '/manage/finance':'财务','/feedback':'意见反馈','/group/admin':'群管理'},'menu':
           ['/order','/manage/sponsor','/manage/orderlist','/manage/finance','/feedback','/group/admin']}

class TopMenu(tornado.web.UIModule):
    def render(self, context):
        path = urlparse.urlsplit(self.request.uri).path.lower()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        menu = []
        
        if path in siteMap['menu']: 
            for pk in siteMap['menu']:
                if not context.identity.isAdmin and pk in ("/group/admin"):
                    continue
                
                if path==pk:   
                    menu.append(temp%(' class="active"',pk,siteMap['pages'][pk]))
                else:
                    menu.append(temp%('',pk,siteMap['pages'][pk]))
        
        if menu:
            return '<div style="height:40px;width:1080px;" align="center"><ul class="topMenu">%s</ul></div>' % ''.join(menu)
        else:
            return ''


