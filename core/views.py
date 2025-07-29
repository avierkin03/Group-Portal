from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from .models import GroupProfile, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Відображає профіль групи (один для всього порталу)
class GroupProfileView(DetailView):
    model = GroupProfile
    template_name = 'core/group_profile.html'
    context_object_name = 'group'

    def get_object(self):
        # Отримуємо перший профіль групи (припускаємо, що є лише один)
        return GroupProfile.objects.first()


# Показує профіль поточного користувача
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'core/user_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Повертаємо профіль поточного користувача
        return self.request.user.profile


# Дозволяє користувачу редагувати власний профіль (біографію, аватар)
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['bio', 'avatar']
    template_name = 'core/user_profile_form.html'
    success_url = reverse_lazy('core:user_profile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Профіль успішно оновлено!')
        return super().form_valid(form)