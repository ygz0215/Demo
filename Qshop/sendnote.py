import requests
url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
#APIID
account = "C09572371"
#APIkey
password = "c5cff620dc119a8e6b66b8566f833eb0"
## 接收人手机号
mobile = "18804661781"
## 发送内容
content = "您的验证码是：1234。请不要把验证码泄露给其他人。"
## 请求头
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
    }
## 构建发送参数
data = {
"account": account,
"password": password,
"mobile": mobile,
"content": content,
}
## 发送请求
response = requests.post(url,headers = headers,data=data)
#url 请求地址
#headers 请求头
#data 发送短信内容
print(response.content.decode())