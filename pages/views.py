from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Page
from .forms import PageForm


# Список усіх опублікованих сторінок
class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    queryset = Page.objects.filter(is_active=True).order_by('-created_at')
    paginate_by = 10


# Відображає статичну сторінку за slug
class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# Створення нової сторінки (лише для адмінів/модераторів)
class PageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:page_list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Сторінку успішно створено!')
        return super().form_valid(form)


# Оновлення сторінки
class PageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:page_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        messages.success(self.request, 'Сторінку успішно відредаговано!')
        return super().form_valid(form)


# Видалення сторінки
class PageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Page
    template_name = 'pages/page_confirm_delete.html'
    success_url = reverse_lazy('pages:page_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        messages.success(self.request, 'Сторінку успішно видалено!')
        return super().form_valid(form)

