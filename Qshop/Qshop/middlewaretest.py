from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class MiddleWareTest(MiddlewareMixin):
    def process_request(self,request):
        rep_ip = request.META.get("REMOTE_ADDR")
        print(rep_ip)
        if rep_ip == "10.10.92.38":  ## 返回响应
            return HttpResponse("同学，请绕路，不支持你访 问！！！")
        print('process_request')

    def process_view(self,request,callback,callbackargs,callbackkwargs):

        version=callbackkwargs.get("date")
        if version == "v1":
            return HttpResponse("版本过期")

        print('process_view')

    def process_exception(self,request,exception):
        print('process_exception')
        from Qshop.settings import BASE_DIR
        import os
        import time
        file=os.path.join(BASE_DIR,'error.log')
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        with open(file,'a') as f:
            content="[%s]:%s \n" %(now_time,str(exception))
            f.write(content)
        pass


    def process_template_response(self,request,response):
        print('process_template_response')
        return response

    def process_response(self,request,response):
        print('process_response')
        print(response)
        return response