from django.urls import path, include

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/bids/', include('bids.urls')),
    path('api/reactivation/', include('reactivation.urls')),
    path('api/admin/', include('adminpanel.urls')),  # If separate admin app
    path('api/referral/',include('referral.urls')),
]
