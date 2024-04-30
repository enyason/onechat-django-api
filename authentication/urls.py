from django.urls import path

from authentication.views import CustomTokenObtainPairView

urlpatterns = [
    path('auth', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
