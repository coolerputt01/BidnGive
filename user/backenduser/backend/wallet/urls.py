from django.urls import path
from .views import WalletBalanceView, DailyBonusView, WithdrawalHistoryView, InvestFromReferralView

urlpatterns = [
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('daily-bonus/', DailyBonusView.as_view(), name='daily-bonus'),
    path('withdrawal-history/', WithdrawalHistoryView.as_view(), name='withdrawal-history'),
    path('invest-from-referral/', InvestFromReferralView.as_view(), name='invest-from-referral'),

]