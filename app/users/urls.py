from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


app_name = 'users_app'


urlpatterns = [
    # authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/google/', views.GoogleAuthView.as_view(), name='login_google'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/all/', views.LogoutAllView.as_view(), name='logout_all'),
    # account
    path('account/email/activate/', views.SendEmailView.as_view(), name='activation_link'),
    path('account/activate/<uidb64>/<token>', views.ActivateEmailView.as_view(), name='activate_email'),
    path('account/password/reset/', views.ResetSendEmailView.as_view(), name='reset_link'),
    path('account/reset/<uidb64>/<token>', views.ResetPasswordView.as_view(), name='reset_password'),
    path('account/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    # profile
    path('user/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('user/<str:username>/follow/', views.FollowUserView.as_view(), name="follow_user"),
    path('<str:uuid>/save/', views.AddFavouritesView.as_view(), name="favourites"),
    path('profile/edit/', views.UpdateProfileView.as_view(), name='update_profile'),
]
