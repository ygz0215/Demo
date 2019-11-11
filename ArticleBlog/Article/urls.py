from  django.urls import path
from .views import *

urlpatterns=[
    path('index/',index),
    path('add/',add),
    path('select/',select),
    path('update/',update),
    path('delete/',delete),
]