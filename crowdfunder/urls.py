"""crowdfunder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('profile/<int:user_id>', profile, name="profile"),
    path('accounts/profile/', account, name="account"),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),    
    path('createproject/', create_project, name="create_project"),
    path('project/<int:id>', project_detail, name="project_detail"),
    path('project/<int:id>/donate/', donate, name="donate"),
    path('project/<int:id>/add-reward/', add_reward, name="add_reward"),
    path('category/<slug:cat>/', category, name="category"),
    path('owner/<int:id>/', projects_by_owner, name="projects_by_owner"),
    path('results/', search_results, name="search_results"),
    url(r'^auth/', include('social_django.urls', namespace='social')), 
    url(r'^$', home, name='home'),
    path('profile_list/', profile_list, name="profile_list"),
]