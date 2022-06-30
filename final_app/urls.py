from . import views
from django.urls import path

urlpatterns=[
    path('',views.towelcome),
    path('index',views.index),
    path('welcome',views.welcome),
    path('register',views. register),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('logout',views.logout),
    path('adding',views.adding),
    path('add_article',views.add_article),
    path('show_article/<int:id>',views.show_article, name="show_article"),
    path('editarticle/<int:id>',views.edit),
    path('delete/<int:id>',views.delete),
    path('search',views.search),
    path('comment',views.comment),
    path('tag/<int:id>',views.tag),
    path('like',views.like_article),
]