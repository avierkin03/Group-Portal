from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    # Список тем форуму
    path('', views.ForumThreadListView.as_view(), name='thread_list'),
    # Деталі теми форуму
    path('thread/<int:pk>/', views.ForumThreadDetailView.as_view(), name='thread_detail'),
    # Створення нової теми
    path('thread/create/', views.ForumThreadCreateView.as_view(), name='thread_create'),
    # Додавання повідомлення до теми
    path('thread/<int:pk>/post/create/', views.ForumPostCreateView.as_view(), name='post_create'),
]