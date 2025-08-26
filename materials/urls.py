from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.MaterialListView.as_view(), name='material-list'),
    path('create/', views.MaterialCreateView.as_view(), name='material-create'),
    path('<int:pk>/update/', views.MaterialUpdateView.as_view(), name='material-update'),
    path('<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material-delete'),
]