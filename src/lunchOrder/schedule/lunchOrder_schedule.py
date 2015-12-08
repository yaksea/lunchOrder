#encoding=utf-8
'''
Created on 2012-6-5

@author: Administrator
'''
from lunchOrder import settings
from lunchOrder.common import log
import sys
import logging
from apscheduler.scheduler import Scheduler
import os
from lunchOrder.schedule import sendEmails
reload(sys)
sys.setdefaultencoding('utf8') 

logging.basicConfig(filename=os.path.join(settings.PATH['log_path'], 'schedule.txt'), level=logging.INFO,
        format='%(levelname)s[%(asctime)s]: %(message)s')


sched = Scheduler(standalone=True)
 
# @sched.interval_schedule(seconds=3)
# def _sendPoints():
#     sendEmails.run()
    
sched.start()

if __name__ == '__main__':    
    pass        
        
        
        
        
        
        
