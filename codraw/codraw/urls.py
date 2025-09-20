"""
URL configuration for codraw project.

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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('signup', views.SignUp,name="SignUp"),
    path('verify',views.Verify,name="Verify"),
    path('signin',views.SignIn,name="SignIn"),
    path('home',views.home,name="home"),
    path('codraw/', views.main,name="main"),
    path('log_out',views.logout,name='logout'),
    path('codraw/settings',views.settings,name='settings'),
    path('codraw/account',views.account,name='account'),
    path('get_project_url',views.get_url,name='get_url'),
    path('board/<str:id>/<str:room>',views.board,name='board'),
    path('codraw/save_project',views.save,name='save'),
    path('codraw/get_boards',views.my_projects,name='my_projects'),
    path('codraw/get_details',views.load,name="load"),
    path('load',views.load_board,name="load_board"),
    path('codraw/save_new',views.save_new,name='save_new'),
    path('codraw/check_owner',views.check_owner,name='check_owner'),
    path('get_popular',views.trending,name="trending"),
    path('search',views.search,name="search"),
    path('username',views.username,name="username")
]
