#encoding=utf-8
'''
Created on 2015年11月24日

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo


def runUser():
    print 'runUser'
    for row in mongo.db['user'].find():
        site = row.get('site')
        if site == 'nd':
            row.update({'passwords':'e10adc3949ba59abbe56e057f20f883e', 'email':'yaksea@gmail.com', 'mobile':'',
                       'address':'', 'site':'pri', '_id':row['_id'].replace('nd_', 'pri_')})
            mongo.db['user'].insert(row)
            
def runUserGroup():
    print 'runUserGroup'
    for row in mongo.db['userGroup'].find():
        site = row.get('site')
        if site == 'nd' or (not site and row.get('userId') and row['userId'].startswith('nd_')):
            mongo.db['userGroup'].update({'_id':row['_id']},{'$set':{'site':'pri', 'userId':row['userId'].replace('nd_', 'pri_')}})

def runGroup():
    print 'runGroup'
    for row in mongo.db['group'].find():
        founder = row['founder']
        admins = row['admins']
        
        if founder.get('site') == 'nd' or founder['userId'].startswith('nd_'):
            founder['site'] = 'pri'
            founder['userId'] = founder['userId'].replace('nd_', 'pri_')
        
        for admin in admins:
            if admin.get('site') == 'nd' or admin['userId'].startswith('nd_'):
                admin['site'] = 'pri'
                admin['userId'] = admin['userId'].replace('nd_', 'pri_')
            
        mongo.db['group'].update({'_id':row['_id']},{'$set':{'founder':founder, 'admins':admins}})
            
def runApply():
    print 'runApply'
    for row in mongo.db['apply'].find():
        founder = row['group']['founder']
        applicant = row['applicant']
        approvers = row['approvers']
        
        if founder.get('site') == 'nd' or founder['userId'].startswith('nd_'):
            founder['site'] = 'pri'
            founder['userId'] = founder['userId'].replace('nd_', 'pri_')
        
        if applicant.get('site') == 'nd' or applicant['userId'].startswith('nd_'):
            applicant['site'] = 'pri'
            applicant['userId'] = applicant['userId'].replace('nd_', 'pri_')
        
        newApprovers = []
        for approver in approvers:
            newApprovers.append( approver.replace('nd_', 'pri_')) 
                       
        mongo.db['apply'].update({'_id':row['_id']},{'$set':{'group.founder':founder, 'applicant':applicant,\
                                                                 'approvers':newApprovers}})
                    
def runTables():
    tables = {'accountLog':'user', 'accountLog_recharge':'user', 'feedback':'user', \
              'order':'sponsor', 'orderDetail':'user' }
#     tables = {'accountLog_recharge':'user'}
    for table, key in tables.items():
        run(table, key)
                
def run(table, key):
    print table
    for row in mongo.db[table].find():
        vv = row.get(key)
        if vv:
            isND = False
            site = vv.get('site')
            if site == 'nd':
                isND = True
            elif not site:
                if vv['userId'].startswith('nd_'):                    
                    isND = True
                    
            if isND:
                vv['site'] = 'pri'
                vv['userId'] = vv['userId'].replace('nd_', 'pri_')
                mongo.db[table].update({'_id':row['_id']},{'$set':{key:vv}})
            


if __name__ == '__main__':
    runUserGroup()
    print 'done.'