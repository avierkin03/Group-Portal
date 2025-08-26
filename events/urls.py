from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
]