"""AizuHandsOff URL Configuration

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
from django.contrib import admin
from django.urls import path

from HandsOffApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main', views.main, name='view-main'),
    path('', views.main),
    path('register', views.register, name='register'),               # show reg form
    path('do_register', views.do_register),                          # send reg information
    path('login', views.login, name='login'),
    path('do_login', views.do_login),
    path('logout', views.logout, name='logout'),
    path('add_item', views.add_item, name='add_item'),
    path('do_add_item', views.do_add_item),
    path('my-items', views.added_items, name='my_items'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:pk>/remove/', views.remove_item, name='remove_item'),
    path('categories/<int:pk>/', views.show_by_category, name='by_category'),
    path('show_by_category_ajax', views.show_by_category_ajax, name='show_by_category_ajax')
    ]
