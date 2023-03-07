from django.urls import path
from .views import login_manage
from .views import register_manage 
from .views import error 
from .views import home 
from .views import market
from .views import usercenter

urlpatterns = [
    path('regster/', login_manage.login.as_view(), name='regster'),
    path('404/', error.pagenotfound.as_view(), name='404'),
    path('index/', home.index.as_view(), name='index'),
    path('login/', login_manage.login.as_view(), name='login'),
    path('main/<str:username>', home.main.as_view(), name='main'),
    path('register/', register_manage.register.as_view(), name='register'),
    path('usercenter/<str:username>', usercenter.usercenter.as_view(), name='usercenter'),
    path('market/', market.market.as_view(), name='market')
]