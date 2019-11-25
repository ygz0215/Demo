from django.http import HttpResponse
from django.shortcuts import render,render_to_response


def hello(request):
    return HttpResponse('hello,xixi')

def abc(request):
    return HttpResponse('aaabbbccc')

# def getday(request,year,month,day):
#     pass

def tpltext(request):
    html="""
    <html>
    <head>
    </head>
    <body>
    <h1>哈哈哈哈哈哈</h1>
    <a href='https://www.baidu.com'>百度一下</a>
    </body>
    </html>
    
    """
    return HttpResponse(html)

def index(request):
    return render(request,'index.html',{'name':'lisi'})

def index2(request):
    return render_to_response('index.html')

def tmptest(request):
    name = "hello"
    age = 10
    hobby=['玩','吃','睡']
    score={'math':100,'english':90,'chinese':99}
    js='''
    <script>
    alert('11111');
    </script>
    '''

    return render(request,"index.html",locals())


