ps -ef|grep main_product|grep 8091|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8092|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8093|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8094|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8095|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8096|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8097|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep main_product|grep 8098|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep schedule/sendEmails.py|grep -v grep|cut -c 9-15|xargs kill -9

rm settings.py
svn update
rm settings.py
mv settings_product.py settings.py

#nohup python main_product.py -port=89>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8091>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8092>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 &  
nohup python main_product.py -port=8093>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8094>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8095>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8096>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8097>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python main_product.py -port=8098>/data/wwwroot/lunchOrder/static/log/access.txt 2>&1 & 
nohup python schedule/sendEmails.py >/data/wwwroot/lunchOrder/static/log/sendEmails.txt 2>&1 &