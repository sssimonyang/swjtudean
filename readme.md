## swjtudean

> 所有代码主要爬虫对象为西南交通大学教务网或扬华网

- `/homepage/jiaowu.py` 教务网主页信息爬取  
- `/homepage/yanghua.py` 扬华网信息爬取  
- `/login/chrome.py` chrome模拟登录教务网  
- `/login/login.py` 利用百度api识别验证码登录教务网  
- `/personal_page/evaluation.py` 教务登陆后个人主页完成课程评价  
- `/personal_page/tuimian.py` 教务登陆后个人主页完成保研课查询  
- `/mail.py` 辅助完成邮件发送 
- `/main.py` 运行程序

涉及到的库  
`baidu-aip lxml openpyxl Pillow psycopg2 requests selenium xlrd` 

> python版本 最低为3.6

安装包
`pip install baidu-aip lxml openpyxl Pillow requests xlrd`
> 除`baidu-aip`之外的所有包都可用`conda`安装

### 自动评价
自动评价涉及的文件为
- `/login/login.py`
- `/personal_page/evaluation.py`
- `/config.py` 需自行创建
- `/main.py`

进入[百度ai开放平台](http://ai.baidu.com/)  
点击控制台 登录 选择左侧文字识别 然后创建应用  
应用的名字和简介随便写，常见成功后会显示`AppID API Key Secret Key`
在该目录下创建`config.py`

-----------
`config.py`
```
APP_ID = '17868961'  # 对应替换为你申请的AppID
API_KEY = 'sZGw4ynaOLIdXoijfI5IFbYX'  # 对应替换为你申请的API Key
SECRET_KEY = '98q8NEoKTWioZzv8Bey7HOEYgiYTDL8I' # 对应替换为你申请的Secret Key
user_id = '201*****' # 对应写入你自己的教务账号
user_password = '*****' # 对应写入你自己的教务密码
```
> 如果不想申请可以直接用我给的，但是一个接口每天使用次数有限制，建议自己申请并进行替换

该目录下运行
`
python main.py
`
或运行时指定
`
python main.py -id <your_user_id> -pw <your_user_password>'
`

#### 启用`mail.py`的功能
在`config.py`加入如下信息
```
mail_username = '****************' # email地址
mail_password = '****************' # email开启smtp服务后提供的登录授权码
mail_host = 'smtp.***.com'  # 对应的smtp服务器
user_email = '****************' # 通知到的email地址
```
然后更改`evaluation`的部分
```
    from mail import send_mail
    if email:
        send_mail(send_tos=[email], name="SSSimon Yang", subject=f"{user_id} 自动评价结果",
                  text=message)
```
然后更改`main.py`的部分
```
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id", help="specify your user id")
    parser.add_argument("-pw", "--password", help="specify your user password")
    parser.add_argument("-email", "--email", help="specify your email address to send to")
    args = parser.parse_args()
    if args.id and args.password:
        process(args.id, args.password, args.email)
    else:
        process(config.user_id, config.user_password, config.user_email)
```
同样，执行
`
python main.py
`
或
`
python main.py -id <your_user_id> -pw <your_user_password>'
`

### 批量化
编辑csv文件
对`/personal_page/evaluation.py`中的`main.py`进行相应更改

Wish you a good day!