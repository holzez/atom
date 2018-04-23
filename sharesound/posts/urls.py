from posts import views
from django.urls import path

urlpatterns = [
    path('sub_post_list.json', views.sub_post_list_json, name="sub_post_list_json"),
    path('', views.subs_track_list, name='sub_posts_list'),
    path('posts/', views.posts_list, name='posts_list'),
    path('post_list.json', views.post_list_json, name="post_list_json"),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:genre_id>', views.genre_post_list, name='genre_post_list'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:tag_id>', views.tag_post_list, name='tag_post_list'),
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>', views.user_detail, name='user_detail'),
    path('albums/', views.album_list, name='album_list'),
    path('album_list.json', views.album_list_json, name="album_list_json"),
]
