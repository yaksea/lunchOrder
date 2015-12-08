'''

@author: Administrator
'''
from lunchOrder.data.mongodbManager import mongo

def run():
    mongo.userGroup.update({'remarkName':None},{'$set':{'remarkName':''}}, multi=True)

if __name__ == '__main__':
    run()