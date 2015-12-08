#encoding=utf-8
import json
from lunchOrder.common.exception import StopOnPurpose
from lunchOrder.base.handlers.logHandler import LogRequestHandler

class JsonRequestHandler(LogRequestHandler):    
    def __init__(self, *args, **kwargs):
        super(JsonRequestHandler, self).__init__(*args, **kwargs)
        self._jsonp = self.params['jsonpcallback']
        
    def responseJson(self, data):
        self.add_header('Cache-Control', 'no-cache')
#        self.add_header("Content-Type", "application/json; charset=UTF-8")
        self.add_header("Content-Type", "text/html; charset=UTF-8")
        if data != None:
            rd = json.dumps(data)#,ensure_ascii=False)
        else:
            rd = ''
        
        if self._jsonp:
            self.write('%s(%s)'%(self._jsonp,rd))
        else:
            self.write(rd)
        self.finish()
           


    def sendMsg(self, message='success', statusCode=200, **kwargs):
        msg = dict(message=message,statusCode=statusCode)
        msg.update(kwargs)
        self.responseJson(msg)
        raise StopOnPurpose()
    
    def sendMsg_WrongParameter(self, message='参数错误', **kwargs):
        self.sendMsg(message, 400, **kwargs)
        
    def sendMsg_NoIdentity(self, message='无法获取身份', **kwargs):
        self.sendMsg(message, 401, **kwargs) #需重登录
        
    def sendMsg_SysUnInit(self, message='系统未开通', **kwargs):
        self.sendMsg(message, 402, **kwargs)
        
    def sendMsg_NoPermission(self, message='无操作权限', **kwargs):
        self.sendMsg(message, 403, **kwargs)
        
    def sendMsg_NoData(self, message='无数据', **kwargs):
        self.sendMsg(message, 404, **kwargs)
        
    def sendMsg_NoEncryptKey(self, message='密钥失效', **kwargs):
        self.sendMsg(message, 406, **kwargs)
        
    def sendMsg_Duplicated(self, message='重复的数据', **kwargs):
        self.sendMsg(message, 409, **kwargs)
        
    def sendMsg_FailToMD5Check(self, message='文件MD5校验失败', **kwargs):
        self.sendMsg(message, 410, **kwargs)
        
    def sendMsg_Unknown(self, message='未知错误', **kwargs):
        self.sendMsg(message, 500, **kwargs)
        
    def sendMsg_VersionTooLow(self, message='版本过低，请升级', **kwargs):
        self.sendMsg(message, 505, **kwargs)
        
    def sendMsg_FailToLogin(self, message='用户名或密码错误', **kwargs):
        self.sendMsg(message, 601, **kwargs)
        
    def sendMsg_ExpiredSecurityCode(self, message='验证码失效', **kwargs):
        self.sendMsg(message, 602, **kwargs)
        
    def sendMsg_WrongSecurityCode(self, message='验证码错误', **kwargs):
        self.sendMsg(message, 603)
        
    def sendMsg_OverLoginTryTimes(self, 
                                  message='由于1小时内连续登录失败次数超过5次，已被暂时禁止登录，请1小时后再试。',
                                  **kwargs):
        self.sendMsg(message, 604, **kwargs)
        
        
        
        
        
    