#encoding=utf-8
'''
Created on 2012-9-22

@author: Administrator
'''
from lunchOrder.common.cache.sessionManager import Session
import base64

from lunchOrder import settings
from lunchOrder.common.exception import SysUnInit, InvalidSessionId
from lunchOrder.base.identity import Identity
from lunchOrder.base.handlers.sessionHandler import SessionRequestHandler
from M2Crypto.EVP import Cipher
from base64 import b64encode
from M2Crypto import m2

IV= '123456'
ALG = 'aes_128_cfb'
PADDING = m2.no_padding


class EncryptRequestHandler(SessionRequestHandler):    
    def __init__(self, *args, **kwargs):
        super(EncryptRequestHandler, self).__init__(*args, **kwargs)
        if self.request.body:
            self.request.body = decrypt(self.request.body, self.encryptKey)     

            
    def write(self, chunk):
        chunk = encrypt(chunk, self.encryptKey)
        super(EncryptRequestHandler, self).write(chunk)

def encrypt(chunk, key):
    cipher = Cipher(alg=ALG, key=key, iv=IV, op=1, key_as_bytes=0,padding=PADDING) # 1 is encrypt
    # padding 有时设置为1
    cipher.set_padding(padding=m2.no_padding)
    v = cipher.update(chunk)
    v = v + cipher.final()
    del cipher #需要删除
    
    return v                  

def decrypt(chunk, key):
    cipher = Cipher(alg=ALG, key=key, iv=IV, op=0, key_as_bytes=0, padding=PADDING) # 0 is decrypt
    cipher.set_padding(padding=m2.no_padding)
    v = cipher.update(chunk)
    v = v + cipher.final()
    del cipher #需要删除
    return v 

if __name__ == '__main__':
    print decrypt(encrypt('#对称加密算法aes', '123'),'123')
     
    