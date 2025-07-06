"""
URL configuration for projectroot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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


from .views import *
from Users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #----Paths that will handle Simple pages-----------------------------------
    
    path('',home,name='landing_page'),
    
    #----Paths that will handle User bases-----------------------------------
    
    path('create-account',create_account,name='create_account_page'),
    path('login',login_account,name='login_account_page'),
    path('logout',logout_account,name='logout_account_page'),
    
    path('profile',user_profile,name='user_profile_page'),
    path('verify-profile',verify_profile,name='verify_profile_page'),
    
    path('upload-profile-picture',upload_profile_image,name='upload_profile_image_page'),
    path('edit-profile',edit_profile,name='edit_profile_page'),
    path('edit-email',edit_email,name='edit_email_page'),
    path('edit-password',edit_password,name='edit_password_page'),
    
    path('forget-email',forget_email,name='forget_email_page'),
    
    path('forget-password',forget_password,name='forget_password_page'),
    
    path('delete-account',delete_account,name='delete_account'),
    
    #----Paths that will handle User bases-----------------------------------
    
]
