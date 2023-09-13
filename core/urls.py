"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import HomeView
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home_url"),
    path('signup/', SignupView.as_view(), name="signup_url"),
    path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', logout_view, name="logout_url"),
    path('profile/', ProfileView.as_view(), name="profile_url"),
    path('add-personal-info/', PersonalInfoView.as_view(), name="personal_info_url"),
    path('verify-phone/', OtpView.as_view(), name='otp_url'),
    path('retotp/<str:phone>', ret_otp),
    path('manage-requests/', manage_requests, name="manage_requests_url"),
    path('delete-user/<int:id>', delete_user, name="delete_user_url")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
