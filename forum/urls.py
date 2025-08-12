from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    # Список тем форуму
    path('', views.TopicListView.as_view(), name='topic_list'),
    # Деталі теми форуму
    path('<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    # Створення нової теми
    path('create/', views.TopicCreateView.as_view(), name='topic_create'),
    # Додавання повідомлення до теми
    path('<int:pk>/post/', views.PostCreateView.as_view(), name='post_create'),
    # Редагування повідомлення до теми (topic_pk для контексту і pk для ID повідомлення)
    path('<int:topic_pk>/post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    # Видалення повідомлення у теми (topic_pk для контексту і pk для ID повідомлення)
    path('<int:topic_pk>/post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]