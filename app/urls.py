from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.auth_page, name='auth_page'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Main pages
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Posts
    path('addposts/', views.addposts, name='addposts'),
    path('view_posts/', views.view_posts, name='view_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),

    # Comments
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # Search
    path('search/', views.search_view, name='search'),

    # Profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
