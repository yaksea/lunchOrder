'''

@author: Administrator
'''
from pymongo.connection import Connection

def run():
    connection = Connection('mongo.duapp.com', 8908)    
#    db = connection['local']
    mongo = connection['KQHKBexgCkvVeJQeZvAK']    
    mongo.authenticate('S3XqY9xdXfi0bKL8xn09lqU2', 'tDMdStgM5XqSIjKnSed7gy2Eg3fi98xg')
    mongo.db['xx'].insert({'sdf':'adf'})
    
if __name__ == '__main__':
    run()