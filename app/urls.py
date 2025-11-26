from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_page, name='auth_page'),

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('addposts/', views.addposts, name='addposts'),
    path('viewposts/', views.viewposts, name='viewposts'),
    path('search/', views.search_view, name='search'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),


    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
