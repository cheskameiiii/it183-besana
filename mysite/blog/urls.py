from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # URL for listing posts
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # URL for viewing a single post
]