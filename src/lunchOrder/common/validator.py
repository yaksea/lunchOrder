'''

@author: Administrator
'''
import re

class Validator():
    class _Method:
        def __init__(self, invoker, method):  
            self._invoker = invoker  
            self._method = method  
      
        def __call__(self, *args, **kwargs): 
            return self._invoker(self._method, *args, **kwargs)
            
    _email = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    _mobile = re.compile(r'^(13|15|18|14|17)\d{9}$', re.I)
    _userName = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{5,15}$', re.I)
    
    def __getattr__(self, name):
        return self._Method(self.__invoker, name)
    
    def __invoker(self, method, val): 
        return getattr(self, "_"+method).match(val) 
    


if __name__ == '__main__':
    vv = Validator()
    print vv.email('dsf@dsaf.com')