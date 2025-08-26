from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from .forms import EventForm, EventFilterForm
from datetime import datetime
from django.contrib import messages

# Список подій
class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/event_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get("date", "")
        if date:
            queryset = queryset.filter(start_date__date=date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventFilterForm(self.request.GET or None)
        return context


# Створення нової події
class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Подію успішно створено!')
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']


# Редагування існуючої події
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event-list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']
    
    def form_valid(self, form):
        messages.success(self.request, 'Подію успішно відредаговано!')
        return super().form_valid(form)


 #Видалення існуючої події
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_delete_confirmation.html'
    success_url = reverse_lazy('events:event-list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']
    
    def form_valid(self, form):
        messages.success(self.request, 'Подію успішно видалено!')
        return super().form_valid(form)