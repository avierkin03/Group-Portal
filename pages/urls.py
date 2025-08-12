from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Список усіх опублікованих сторінок
    path('', views.PageListView.as_view(), name='page_list'),
    # Створення нової сторінки (лише для адмінів/модераторів)
    path('create/', views.PageCreateView.as_view(), name='page_create'),
    # Відображення конкретної сторінки за slug
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    # Редагування сторінки
    path('<slug:slug>/edit/', views.PageUpdateView.as_view(), name='page_edit'),
    # Видалення сторінки
    path('<slug:slug>/delete/', views.PageDeleteView.as_view(), name='page_delete'),
]
