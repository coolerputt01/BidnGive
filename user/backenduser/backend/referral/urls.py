from django.urls import path
from .views import ReferralBonusListView, RequestReferralWithdrawal , LoginBonusView

urlpatterns = [
    path('bonuses/', ReferralBonusListView.as_view(), name='referral-bonuses'),
    path('withdraw/', RequestReferralWithdrawal.as_view(), name='withdraw-referral'),
    path('daily-login/', LoginBonusView.as_view(), name='daily-login-bonus'),
]