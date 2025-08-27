from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PortfolioItem
from .forms import PortfolioItemForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Список проектів поточного користувача
class PortfolioListView(LoginRequiredMixin, ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_items'
    paginate_by = 6

    def get_queryset(self):
        return PortfolioItem.objects.filter(user=self.request.user).order_by('-created_at')


# Список проектів з портфоліо чужого користувача
class UserPortfolioView(LoginRequiredMixin, ListView):
    model = PortfolioItem
    template_name = 'portfolio/user_portfolio.html'
    context_object_name = 'portfolio_items'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return PortfolioItem.objects.filter(user=user, is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username']).profile
        return context
    

# Створення новго проекту у портфоліо
class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Проєкт додано до портфоліо!')
        return super().form_valid(form)


# Оновлення проекту у портфоліо поточного користувача
class PortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

    def form_valid(self, form):
        messages.success(self.request, 'Проєкт оновлено!')
        return super().form_valid(form)


# Видалення проекту з портфоліо поточного користувача
class PortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

    def form_valid(self, form):
        messages.success(self.request, 'Проєкт видалено з портфоліо!')
        return super().form_valid(form)