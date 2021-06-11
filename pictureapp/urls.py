from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/<int:id>', views.profile),
    path('profile/edit/<int:id>', views.profile_edit),
    path('register', views.register),
    path('register_page', views.register_page),
    path('login', views.login),
    path('wall', views.success),
    path('logout', views.logout),
    path('create_post', views.create_post),
    path('create_comment/<int:id>', views.create_comment)
]
