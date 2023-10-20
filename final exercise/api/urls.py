from django.urls import path
from api.views import UserRegisterView, UserLogin, UserProfile
from knox import views as knox_views


urlpatterns = [
    path('user/register', UserRegisterView.as_view()),
    path('login', UserLogin.as_view()),
    path('account', UserProfile.as_view()),
    path('logout',knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logoutall',knox_views.LogoutAllView.as_view(), name='knox-logout-all'),
]