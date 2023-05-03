from django.urls import path
from webexchange.views import (
    login_manage,
    error,
    home,
    register_manage,
    asset,
    usercenter,
    verifyresult,
    wallet_manage,
    nav,
    exchange,
    coins,
    swap,
)

urlpatterns = [
    path("404/", error.pagenotfound.as_view(), name="404"),
    path("", home.index.as_view(), name="index"),
    path("login/", login_manage.login.as_view(), name="login"),
    path("main/<str:username>/", home.main.as_view(), name="main"),
    path("register/", register_manage.register.as_view(), name="register"),
    path(
        "usercenter/<str:username>/", usercenter.usercenter.as_view(), name="usercenter"
    ),
    path("asset/<str:username>/", asset.asset.as_view(), name="asset"),
    path(
        "verifyresult/<str:username>/",
        verifyresult.verifyresult.as_view(),
        name="verifyresult",
    ),
    path("wallet/<str:username>", wallet_manage.wallet.as_view(), name="wallet"),
    path("nav/", nav.nav.as_view(), name="nav"),
    path("exchange/", exchange.exchange.as_view(), name="exchange"),
    path("coins/", coins.coins.as_view(), name="coins"),
    path("swap/", swap.swap.as_view(), name="swap"),
]
