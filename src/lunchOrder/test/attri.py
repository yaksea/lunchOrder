class Obj(object):  
    photo = "hello"  
    def __getattribute__(self, name):  
        print '1'+name  
        #return _Method(self.__invoke, name)  
        return object.__getattribute__(self, name)  
  
    def __getattr__(self, name):  
        print '2'+name  
        return _Method(self.__invoke, name)  
  
    def __invoke(self, method, params): 
        print params 
        print 'invoke'  
  
class _Method:  
    def __init__(self, invoker, method):  
        self._invoker = invoker  
        self._method = method  
  
    def __call__(self, *args):  
        return self._invoker(self._method, args)  
  
o = Obj()  
# print o.photo  
o.xx('cvb', 'dfg')  