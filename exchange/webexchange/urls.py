from django.urls import path
from webexchange.views import (
    login_manage,
    error,
    home,
    register_manage,
    asset,
    usercenter,
    verifyresult,
    transaction,
    nav,
    exchange,
    coins,
    swap,
    proof,
    wallet,
    walletlogin,
    trade,
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
    path("transaction/<str:username>", transaction.transaction.as_view(), name="transaction"),
    path("nav/", nav.nav.as_view(), name="nav"),
    path("exchange/", exchange.exchange.as_view(), name="exchange"),
    path("coins/", coins.coins.as_view(), name="coins"),
    path("swap/", swap.swap.as_view(), name="swap"),
    path("proof/", proof.proof.as_view(), name="proof"),
    path("walletlogin/", walletlogin.walletlogin.as_view(), name="walletlogin"),
    path("trade/<str:username>/", trade.trade.as_view(), name="trade"),
    path("wallet/<str:username>/", wallet.wallet.as_view(), name="wallet"),
]
