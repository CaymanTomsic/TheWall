from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('wall', views.wall),
    path('create_message', views.create_message),
    path('destroy_message/<int:message_id>', views.destroy_message),
    path('create_comment/<int:message_id>', views.create_comment),
    path('logout', views.logout),
]
