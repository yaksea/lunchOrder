#encoding=utf-8

class dev():
    class nd():
        client = {
            'apiUrl': 'http://oapnd.91.com'
            }

        server = {
#                   'apiUrl': 'http://oapsnd.99.com',
#                   'auth':{"id":1063,"key":"349cdff1-2abc-4941-bd34-21c20cdd4644"},
                    'apiUrl': 'http://192.168.9.76/oaps',
                    'auth':{"id":45, "key":"7e7fe7e1-8aeb-415b-beca-824bb1656c9a"},
                'initForwardDays': 3  # days ago
                }
        
        db = {
            'host' : '192.168.19.184',
            'port': 27017,
            'db_name' : 'alumnus_voting',
            'prefix': 'nd_'
          }
        
    class yb():
        client = {
            'apiUrl': 'http://192.168.94.21/oap/'
#            'apiUrl': 'http://oapnd.91.com'
            }

        server = {
#                    'apiUrl': 'http://oaps.99.com',
#                    'auth':{"id":1063,"key":"7a8c1e6f-72ac-4433-895c-7b40aef7b652"},                  
                    'apiUrl': 'http://192.168.94.21/oaps',
                    'auth':{"id":10102,"key":"a42e0886-1021-498a-9fff-df3fa234e777"},
                    'initForwardDays': 3  # days ago
                    }
        db = {
            'host' : '192.168.19.184',
            'port': 27017,
            'db_name' : 'alumnus_voting',
            'prefix': 'yb_'
          }
                
    class jm():
        client = {
            'apiUrl': 'http://192.168.9.76/oap/'
#            'apiUrl': 'http://oapnd.91.com'
            }

        server = {
                    'apiUrl': 'http://192.168.94.21/oaps',
                    'auth':{"id":10102,"key":"a42e0886-1021-498a-9fff-df3fa234e777"},
                    'initForwardDays': 3  # days ago
                    }
        db = {
            'host' : '192.168.19.184',
            'port': 27017,
            'db_name' : 'alumnus_voting',
            'prefix': 'jm_'
          }
        
class pro():
    class nd():
        client = {
            'apiUrl': 'http://oapnd.99.com'
            }

        server = {
                'apiUrl': 'http://oapsnd.99.com',
                'auth':{"id":1063, "key":"349cdff1-2abc-4941-bd34-21c20cdd4644"},
                'initForwardDays': 3  # days ago
                }
        db = {
                'host' : '10.1.250.156',
                'port': 27017,
                'db_name' : 'alumnus_voting',
                'user_name' : 'alumnus_voting',
                'passwords' : 'BaKbvArzprTVbXsm',
            'prefix': 'nd_'
              }        
        
    class yb():
        client = {
            'apiUrl': 'http://121.207.250.159'
            }
        
        server = {
                    'apiUrl': 'http://oaps.99.com',
                    'auth':{"id":1063,"key":"7a8c1e6f-72ac-4433-895c-7b40aef7b652"},
                    'initForwardDays': 3  # days ago
                    }
        db = {
                'host' : '10.1.250.156',
                'port': 27017,
                'db_name' : 'alumnus_voting',
                'user_name' : 'alumnus_voting',
                'passwords' : 'BaKbvArzprTVbXsm',
                'prefix': ''
              }        
        
    class jm():
        client = {
                  'apiUrl': 'oap99.jmu.cn'
            }

        server = {
                    'apiUrl': 'oaps99.jmu.cn/apis',
                    'auth':{"id":1063,"key":"7a8c1e6f-72ac-4433-895c-7b40aef7b652"},
                    'initForwardDays': 3  # days ago
                    }
        db = {
                'host' : '10.1.250.156',
                'port': 27017,
                'db_name' : 'alumnus_voting',
                'user_name' : 'alumnus_voting',
                'passwords' : 'BaKbvArzprTVbXsm',
            'prefix': 'jm_'
              }  
        
class emu():#仿真
    class nd():
        client = {
            'apiUrl': 'http://oapnd.91.com'
            }

        server = {
                'apiUrl': 'http://oapsnd.91.com',
                'auth':{"id":1063, "key":"349cdff1-2abc-4941-bd34-21c20cdd4644"},
                'initForwardDays': 3  # days ago
                }
        db = {
                'host' : '10.123.247.85',
                'port': 37017,
                'db_name' : 'voting_xy',
                'user_name' : 'lunchOrder',
                'passwords' : 'BaKbvArzprTVbXsm',
            'prefix': 'nd_'
              }        
        
    class yb():
        client = {
            'apiUrl': 'http://192.168.9.76/oap/'
            }

        server = {
                    'apiUrl': 'http://192.168.9.76/oaps',
                    'auth':{"id":45, "key":"7e7fe7e1-8aeb-415b-beca-824bb1656c9a"},
                    'initForwardDays': 3  # days ago
                    }
        db = {
                'host' : '10.123.247.85',
                'port': 37017,
                'db_name' : 'voting_xy',
                'user_name' : 'lunchOrder',
                'passwords' : 'BaKbvArzprTVbXsm',
            'prefix': 'yb_'
              } 
                
    class jm():
        client = {
                  'apiUrl': 'oap99.jmu.cn'
            }

        server = {
                    'apiUrl': 'oaps99.jmu.cn/apis',
                    'auth':{"id":45, "key":"7e7fe7e1-8aeb-415b-beca-824bb1656c9a"},
                    'initForwardDays': 3  # days ago
                    }
        
        db = {
                'host' : '10.123.247.85',
                'port': 37017,
                'db_name' : 'voting_xy',
                'user_name' : 'lunchOrder',
                'passwords' : 'BaKbvArzprTVbXsm',
            'prefix': 'jm_'
              }         
