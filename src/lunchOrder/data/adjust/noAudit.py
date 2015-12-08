'''

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def run():
    mongo.group.update({},{'$set':{'noAudit':1}}, multi=True)

if __name__ == '__main__':
    run()