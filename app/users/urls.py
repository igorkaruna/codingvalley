from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users import views
from users.views import UserTokenObtainPairView


urlpatterns = [
    path('', views.getRoutes),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
