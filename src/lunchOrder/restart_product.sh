ps -ef|grep main_product|grep 8041|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8042|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8043|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8044|grep -v grep|cut -c 9-15|xargs kill -9

rm settings.py
svn update
rm settings.py
mv settings_product.py settings.py

nohup python main_product.py -port=8040>/data/wwwroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8041>/data/wwwroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8042>/data/wwwroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8043>/data/wwwroot/lunchOrder/log.txt 2>&1 &
nohup python main_product.py -port=8044>/data/wwwroot/lunchOrder/log.txt 2>&1 &