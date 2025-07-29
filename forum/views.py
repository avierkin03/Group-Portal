from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ForumThread, ForumPost

# Список тем форуму, із сортуванням закріплених тем першими
class ForumThreadListView(ListView):
    model = ForumThread
    template_name = 'forum/thread_list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        # Показуємо закріплені теми першими
        return ForumThread.objects.all().order_by('-is_pinned', '-created_at')


# Відображає тему та її повідомлення
class ForumThreadDetailView(DetailView):
    model = ForumThread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        return context


# Створення нової теми (доступно для всіх автентифікованих користувачів)
class ForumThreadCreateView(LoginRequiredMixin, CreateView):
    model = ForumThread
    fields = ['title']
    template_name = 'forum/thread_form.html'
    success_url = reverse_lazy('forum:thread_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Тему успішно створено!')
        return super().form_valid(form)


# Додавання повідомлення до теми
class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    fields = ['content']
    template_name = 'forum/post_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.thread = get_object_or_404(ForumThread, pk=self.kwargs['pk'])
        messages.success(self.request, 'Повідомлення додано!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.kwargs['pk']})
