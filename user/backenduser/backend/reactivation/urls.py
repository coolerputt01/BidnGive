from django.urls import path
from .views import RequestReactivationView
from .admin_views import ListDisabledUsersView, ApproveReactivationView

urlpatterns = [
    path('request/', RequestReactivationView.as_view(), name='reactivation-request'),
    path('disabled/', ListDisabledUsersView.as_view(), name='list-disabled-users'),
    path('approve/<int:user_id>/', ApproveReactivationView.as_view(), name='approve-reactivation'),
]
