from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Page


# Відображає статичну сторінку за slug
class PageView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'

    def get_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'], is_published=True)


# Створення нової сторінки (лише для адмінів/модераторів)
class PageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Page
    fields = ['title', 'slug', 'content', 'is_published']
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:page_list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        messages.success(self.request, 'Сторінку успішно створено!')
        return super().form_valid(form)


# Список усіх опублікованих сторінок
class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)
