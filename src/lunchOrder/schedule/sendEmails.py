#encoding=utf-8
'''
Created on 2013-5-27

@author: Alex
'''
import smtplib
from email.mime.text import MIMEText
from lunchOrder import settings
import time
import json
import traceback
from lunchOrder.data.redisManager import redisDb
from lunchOrder.common import log
from email.mime.multipart import MIMEMultipart

def init():
    smtpserver = smtplib.SMTP(settings.EMAIL['host'])
    smtpserver.starttls()
    smtpserver.login(settings.EMAIL['user'], settings.EMAIL['password'])
    return smtpserver
    
    
def run():
    queue = redisDb.emailQueue
    smtpserver = init()
    while 1:
        while not queue.isEmpty():
            item = queue.pop()
            log.out(item['to'])
            msg = MIMEMultipart() 
                
            msg['From'] = '一起叫餐吧<%s>'%settings.EMAIL['user']
            if type(item['to']) == list:
                item['to'] = ';'.join(item['to']) 
            
            msg['To'] = item['to']
            msg['Subject']= item['subject']
            
            if item['content'].startswith('<'):
                msg.attach(MIMEText(item['content'], 'html','utf-8'))
            else:  
                msg.attach(MIMEText(item['content'],'text','utf-8'))
                
            try:
                if not smtpserver:
                    smtpserver = init()
                    
                smtpserver.sendmail(settings.EMAIL['user'], item['to'], msg.as_string())
            except:
                traceback.print_exc() 
#                 queue.push(item)
                smtpserver = None
        
        if smtpserver:
            smtpserver.quit()
            smtpserver = None
            
        time.sleep(1.5)


        
def test():
        smtpserver = init()
        
        item = {'to':'37144326@qq.com', 'subject': 'test_test'}   
        item['content'] = '''<html><body><div style="padding:16px 0px 6px 0px">您好，%s：</div>
                            <div style="padding-left:40px;line-height:28px;"><a href="http://17j38.com/user/resetpasswords?rid=%s&uid=%s">请点此将密码重置为：123456</a></div>
                           <div style="padding-left:40px;line-height:28px;">或直接使用浏览器打开以下地址：http://17j38.com/user/resetpasswords?rid=%s&uid=%s</div>
                           <div style="color:red;padding-left:40px;line-height:28px;">该键接地址仅在1小时内有效，有效期至%s</div>
                           <div style="padding:16px 0px 0px 40px;">感谢您使用 [一起叫餐吧]  http://17j38.com</div>
                                
                        '''        
        
        msg = MIMEMultipart() 
        
            
        msg['From'] = '一起叫餐吧<%s>'%settings.EMAIL['user']
        if type(item['to']) == list:
            item['to'] = ';'.join(item['to']) 
        
        msg['To'] = item['to']
        msg['Subject']= item['subject']
        
        print item['to']
        if str(item['content']).startswith('<'):
            msg.attach(MIMEText(item['content'], 'html','utf-8'))
        else:  
            msg.attach(MIMEText(item['content'],'text','utf-8'))
        
        try:
            smtpserver.sendmail(settings.EMAIL['user'], item['to'], msg.as_string())
        except:
            traceback.print_exc()  
            smtpserver = init()
        
        print 'done.'
    
    
    
    
if __name__ == '__main__':
    run()
#     for i in range(3):
#         test()
    




    
    