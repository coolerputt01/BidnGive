from django.urls import path
from .views import WalletBalanceView, DailyBonusView

urlpatterns = [
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('daily-bonus/', DailyBonusView.as_view(), name='daily-bonus'),
]