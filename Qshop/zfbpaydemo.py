from alipay import AliPay
alipay_public_key_string="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzlV3HoHYrLXrzpsXCSMCZpWVR8CLYjv5Y84UHRu5yOC0l01RkWVem/vXRCYl0BumJ8ILot/F1Q4/u9Ed5nH3mWOdm+GAWAp10xl6eJjlwetO0KuLsSIVIvf+37YibgA8I2l2OSER2dV/KQg8Lqg827mc+66SxdpWIKDv0iu7POQ2D4qczBc5C2+xTuDSkgCX8FBwlrCbMlTswwlNSs/LMjiIYsBzS3Iw36u0TrJpc3dZesDz9TJMNmHtiwJaBCiW3mkrlyIaMQwJQEalhyNc3kGNaRMgDmG0SUyJ058GLbFOQlRmZ3xvWHavNdrYELA6uIfmCp+ZCj09gumksM/HvQIDAQAB
-----END PUBLIC KEY-----"""
app_private_key_string ="""-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAzlV3HoHYrLXrzpsXCSMCZpWVR8CLYjv5Y84UHRu5yOC0l01RkWVem/vXRCYl0BumJ8ILot/F1Q4/u9Ed5nH3mWOdm+GAWAp10xl6eJjlwetO0KuLsSIVIvf+37YibgA8I2l2OSER2dV/KQg8Lqg827mc+66SxdpWIKDv0iu7POQ2D4qczBc5C2+xTuDSkgCX8FBwlrCbMlTswwlNSs/LMjiIYsBzS3Iw36u0TrJpc3dZesDz9TJMNmHtiwJaBCiW3mkrlyIaMQwJQEalhyNc3kGNaRMgDmG0SUyJ058GLbFOQlRmZ3xvWHavNdrYELA6uIfmCp+ZCj09gumksM/HvQIDAQABAoIBAQC2EPoUZFUySTCzVWylNkw3AwT/lGopm2w7YiujZ8Su+YDBBYvVNVKfZ0ETNGonUU5zRKmJ5dUmY/VfIG422xe1NQ5s7zWV+lzvkkrcQWZzj9QzEzwnaECoY5Z2BrwovnJSeQvF62VaBya2qTqZnQBejlF0UB3ZEgjvr7MOjGIinlMOqPr+avp/zOlSVD2lYO0lil5Uz46zkeSEqQoP5cRwF/M6OsI7LIdX84IrmWQD/RifW1//Rh3t3lD3ZOrMxT7PHKfb/t2sfQ72YY2KXsFiFqyM/7TwXeXv8nJLmuyLgFc1NwDJZEwFblFYUiL5g5Xjy8S7cp8WWbBIMhKZ4WxBAoGBAO/3DLIrwCBhvjKwLbHWftlVfGFOM9ci9fHqekoqaIdbwvK0qOeYdfItvqARmhhh3gIdF2pHeFkwWCtqSDiDfFoETjjMKMrp4f+tLjuCTd9BDDqVWIFjITEQq5yHfLaQGfEMPNHa+OsP+77ly2uSvidbw0A38nRNNKwkmqe/1P/xAoGBANwfGvuEdKVZVd8lbaGFGAwAblcZXBNlu1CJ0N3/uIJnJ0f/OizECeG4Zhc7EKRpSRIuXssb40ywe9xoKL5bIOeVvm6RqSU5z0Iu4fJTgatiSWfCNfg8qmxqL3mFm1X5nxcZ1IgBgYpgK9Pby7/TDt21E4yrLbAXV5NLace8O9CNAoGBAM9d1JDbkenpzW0MJlC6JWA2qYeFBvNw+MyXbhpNT4s5VtxaFmQcskAYG9VDoMBVQn7dGPD01iFsz6Sk8cg0h+9aLSaT9uRy/KPvyjYOwrCdC65MhPE68uHtn/9ibfltyZ0ukBhhfB3V8Bzlg8ZwRvbIK5CBSHoMheoEr8kq0yxhAoGANooGd3c0J5vg6O8vIKwHb0HUFQSVicDVDnl3JOotXzILy4zzbxALmr/Dm9Hop7PmhPi0SALa6K95oPy1y6RsnLS/gEna7PxL3Awds5r5L+ukYG8ATEdLupz8slFmUYEN5/1gaWpmHFEDyvRUoWy77DbnZx0qrsy5yCcRSIndECkCgYEAnCkwvFtXVO2pbhMaG8OuIa/B+q98v468uUZdBepaNvlHoIqhvz+/l8OeFfkCZqsfJOXoZaqkMfYCaDyISpqfg2F0z4UEsFVEv0J7MWFgSqUtUnTzNk8LU6YOqpZK2zDlGrhZ92ewX+v7VLLcyGX2Y1rc0yWWDBwfNI10+vdO0vg=
-----END RSA PRIVATE KEY-----"""



alipay=AliPay(
    appid="2016101600701596",
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
    debug=False
)

order_string=alipay.api_alipay_trade_page_pay(
    subject='生鲜交易',  ## 交易主题
    out_trade_no='13244768918879',  ## 订单号
    total_amount='998',  ## 交易总金额  需要是一个string
    return_url=None,  ## 返回的路径
    notify_url=None
)

result = "https://openapi.alipaydev.com/gateway.do?" + order_string
print(result)