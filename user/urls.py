from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('create/', views.create, name="create"),
    path('show_videos/<str:slug>', views.show_videos, name="show"),
    path('edit_post/<int:id>', views.editpost, name="edit-post"),
    path('delete_post/<int:id>', views.deletepost, name="delete-post"),
    path('user/profile/<int:id>', views.userprofile, name="users-profile"),
    path('search/', views.search, name='search'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)