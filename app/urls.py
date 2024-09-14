from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('accept/<int:inv>/',views.accept, name="accept"),
    path('delete/<int:inv>/',views.delete, name="delete"),
    path('add/<int:friendid>/', views.add, name="add"),
    path('invitations/', views.invitations, name="display"),
    path('friends/', views.friends, name="friends"),
    path('message/<int:friend_id>/', views.message, name="message"),
    path('search/', views.search_view, name="search"),
    path('addpost/', views.addpost, name="addpost"),
    path('profile/<str:profile_name>/', views.profile, name="profile"),
]