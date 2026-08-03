from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:category>/', views.category_posts, name='category_posts'),
]
