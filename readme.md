所有代码主要针对对象为西南交通大学教务网或扬华网

/homepage/jiaowu.py 教务网主页信息爬取
/homepage/yanghua.py 扬华网信息爬取
/main/chrome.py chrome模拟登录教务网
/main/login.py 利用百度api识别验证码登录教务网
/personal_page/evaluation.py 教务登陆后主页完成课程评价
/personal_page/tuimian.py 教务登陆后完成保研课查询
mail.py 辅助完成邮件发送

requirements
baidu-aip==2.2.17.0
hyper==0.7.0
lxml==4.4.1
openpyxl==3.0.0
Pillow==6.1.0
psycopg2==2.8.3
requests==2.22.0
selenium==3.141.0
xlrd==1.2.0