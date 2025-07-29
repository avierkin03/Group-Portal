from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Список усіх опублікованих сторінок
    path('', views.PageListView.as_view(), name='page_list'),
    # Відображення конкретної сторінки за slug
    path('<slug:slug>/', views.PageView.as_view(), name='page_detail'),
    # Створення нової сторінки (лише для адмінів/модераторів)
    path('create/', views.PageCreateView.as_view(), name='page_create'),
]