from django.urls import path
from . import views

app_name = 'voting'
urlpatterns = [
    # Список активних голосувань
    path('', views.VoteListView.as_view(), name='vote_list'),
    # Деталі голосування
    path('<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),
    # Створення нового голосування (лише для адмінів/модераторів)
    path('create/', views.VoteCreateView.as_view(), name='vote_create'),
    # Обробка голосування
    path('<int:pk>/vote/', views.VoteCastView.as_view(), name='vote_cast'),
]