from django import template

register=template.Library()

@register.filter()
def myadd(a):

    return a+a

@register.filter()
def mymangadd(a,b):

    return a+b


@register.simple_tag()
def myalladd(a,b,c,d):

    return a+b+c+d