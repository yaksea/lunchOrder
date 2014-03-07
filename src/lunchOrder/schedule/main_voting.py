#encoding=utf-8
'''
Created on 2012-6-5

@author: Administrator
'''
import datetime
from lunchOrder.common.utility import *
import time
from lunchOrder.settings import PATH
from lunchOrder import settings
from lunchOrder.common import log
import traceback
from lunchOrder.data.mongodbManager import mongo
import sys
from lunchOrder.logMonitor.analysis.main import runCurrent
reload(sys)
sys.setdefaultencoding('utf8') 

class ScheduleTasks():
        
    def executeDaily(self):
        
        dt = time.time()
        log.out('    clean todayPolls start at %s'%getFormattedTime(dt))
        try:
            mongo.db['voter'].update({},{'$set':{'todayPolls':{'1':0,'2':0,'3':0,'4':0}}}, multi=True)
        except:
            traceback.print_exc()                  
        log.out('    done todayPolls in %d seconds'% (time.time()-dt))

        
        
    
    def executeMinutely(self):
        pass
#        dt = time.time()
#        log.out('    oap sync [half full] start at %s'%(getFormattedTime(dt)))
#        try:            
#            pass
#            
#        except:
#            traceback.print_exc()    
#        log.out('    done oap sync [half full] in %d seconds.'% (time.time() - dt))
    

    def executeTenSecondly(self):
        pass
#        dt = time.time()
#        log.out('    oap sync [increment] start at %s'%(getFormattedTime(dt)))
#        try:            
#            pass
#        except:
            traceback.print_exc()    
#        log.out('    done oap sync [increment] in %d seconds.'% (time.time() - dt))
        


if __name__ == '__main__':    
    lastDailyTaskCode = None
    lastMinutelyTaskCode = None
    lastTenSecondlyTaskCode = None
    tasks = ScheduleTasks()

    while 1:
        log.out('    pulse at %s' % (getFormattedTime(time.time())))

        #daily task
        dailyTaskCode = getDateCode()
        if lastDailyTaskCode != dailyTaskCode:  
            lastDailyTaskCode = dailyTaskCode
            dt = time.time()
            log.out('Daily task [%s] start at %s' % (dailyTaskCode, getFormattedTime(dt)))
            tasks.executeDaily()
            

            dt = time.time() - dt
            log.out('Finished daily task [%s] in %d seconds' % (dailyTaskCode, dt))

        
                        
        time.sleep(10)
        
        
        
        
        
        
        
