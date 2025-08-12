from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
import logging
from .models import Topic, Post
from .forms import TopicForm, PostForm
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

# Список тем форуму
class TopicListView(ListView):
    model = Topic
    template_name = 'forum/topic_list.html'
    context_object_name = 'topics'
    queryset = Topic.objects.filter(is_active=True).order_by('-created_at')


# Відображає тему та її повідомлення
class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо форму для створення повідомлення
        context['form'] = PostForm()
        context['posts'] = self.object.posts.all()[:self.paginate_by]
        logger.debug(f"Context for TopicDetailView: {context}")
        return context


# Створення нової теми (доступно для всіх автентифікованих користувачів)
class TopicCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'
    success_url = reverse_lazy('forum:topic_list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Тему успішно створено!')
        return super().form_valid(form)


# Додавання повідомлення до теми
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def form_valid(self, form):
        form.instance.topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Повідомлення опубліковано!')
        logger.debug(f"Post created by {self.request.user} for topic {form.instance.topic}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.kwargs['pk']})
    

# Редагування повідомлення до теми
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_edit.html'

    def test_func(self):
        post = self.get_object()
        # Дозволяємо редагування автору лише протягом 30 хвилин після створення
        if self.request.user == post.created_by and (timezone.now() - post.created_at) < timedelta(minutes=30):
            return True
        # Дозволяємо редагувати модераторам або адмінам
        return self.request.user.profile.role in ['moderator', 'admin']

    def form_valid(self, form):
        messages.success(self.request, 'Повідомлення успішно відредаговано!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.topic.pk})


# Видалення повідомлення у теми
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        # Дозволяємо видаляти автору, модераторам або адмінам
        return self.request.user == post.created_by or self.request.user.profile.role in ['moderator', 'admin']

    def form_valid(self, form):
        messages.success(self.request, 'Повідомлення успішно видалено!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.topic.pk})
