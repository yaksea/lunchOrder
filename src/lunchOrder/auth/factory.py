#encoding=utf-8
'''

@author: Administrator
'''
from lunchOrder.auth import api
from lunchOrder import settings
from lunchOrder.api import oap, qq, pri

class Site(object):
    yb = 'yb' #云办公
    nd = 'nd' #网龙
    jm = 'jm' #集大
    qq = 'qq'
    pri = 'pri'
    
class User(object):
    instances = {}
    
    @classmethod
    def getApi(cls, site, env=settings.ENVIRONMENT['env']):
        userApi =  cls.instances.get(site)
        if not userApi:
            if site == Site.nd:
                cls.instances[site] = userApi =oap.user.User_nd(env)
            elif site == Site.yb:
                cls.instances[site] = userApi =oap.user.User_yb(env)
            elif site == Site.jm:
                cls.instances[site] = userApi =oap.user.User_jm(env)
            elif site == Site.qq:
                cls.instances[site] = userApi =qq.user.User(env)
            elif site == Site.pri:
                cls.instances[site] = userApi = pri.user.User(env)
            else:
                raise Exception('wrong argument')
                
        return userApi
    


if __name__ == '__main__':
#     user = User.getApi(Site.nd).login(515253, 'abcd1234')
#     user = User.getApi(Site.yb).login('tqnd515253', '1')
#     print user
    user = User.getApi(Site.nd).login(515253, 'weirh123456')
#     print User.getApi(Site.nd).getInfo(user['userId'], user['sessionId'])
#     print User.getApi(Site.yb).login('tqnd515253', '1')
#     print User.getApi(Site.yb).getIdentities('u6lok46ubneqt637l5gdhp2pu5')
    print user
#     print User.getApi(Site.nd).check('lbpsdehq12mmsmsa6tki84r7q7')
#     print dir(userApi)
    pass
