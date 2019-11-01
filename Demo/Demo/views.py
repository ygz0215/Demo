from django.http import HttpResponse

def hello(request):
    return HttpResponse('hello,xixi')

def abc(request):
    return HttpResponse('aaabbbccc')