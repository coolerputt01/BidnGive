from django.http import JsonResponse
from django.urls import path, include
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/admin/token/', CustomTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('', lambda request: JsonResponse({"status": "API is live 🚀"})),
    path('api/wallet/', include('wallet.urls')),
    path('api/bids/', include('bids.urls')),
    path('api/reactivation/', include('reactivation.urls')),
    path('api/admin/', include('adminpanel.urls')),  # If separate admin app
    path('api/referral/',include('referral.urls')),
]
