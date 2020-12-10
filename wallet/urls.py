from django.urls import path, include
from . import views

urlpatterns = [
    path('v1/init/', views.ClientLogin, name="login"),
    path('v1/wallet/', views.MyWallet.as_view(), name="wallet"),
    path('v1/wallet/deposits/', views.Deposits.as_view(), name="deposits"),
    path('v1/wallet/withdrawals/', views.Withdrawal.as_view(), name="withdrawal"),
    
]