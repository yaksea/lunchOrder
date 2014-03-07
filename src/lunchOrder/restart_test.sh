ps -ef|grep main_product|grep 8041|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8042|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8043|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8044|grep -v grep|cut -c 9-15|xargs kill -9

nohup python main_product.py -port=8040>/data/webroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8041>/data/webroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8042>/data/webroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8043>/data/webroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8044>/data/webroot/lunchOrder/log.txt 2>&1 &