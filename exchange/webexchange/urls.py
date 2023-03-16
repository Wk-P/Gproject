from django.urls import path
from webexchange.views import login_manage, error, home, register_manage, market, asset, usercenter, verifyresult, testing

urlpatterns = [
    path('regster/', login_manage.login.as_view(), name='regster'),
    path('404/', error.pagenotfound.as_view(), name='404'),
    path('', home.index.as_view(), name='index'),
    path('login/', login_manage.login.as_view(), name='login'),
    path('main/<str:username>', home.main.as_view(), name='main'),
    path('register/', register_manage.register.as_view(), name='register'),
    path('usercenter/<str:username>', usercenter.usercenter.as_view(), name='usercenter'),
    path('market/', market.market.as_view(), name='market'),
    path('asset/<str:username>', asset.asset.as_view(), name='asset'),
    # path('testing/', testing.testing.as_view(), name='testing'),
    path('verifyresult/<str:username>', verifyresult.verifyresult.as_view(), name='verifyresult')
]