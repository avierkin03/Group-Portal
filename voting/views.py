from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Vote, VoteOption, UserVote
from django.http import HttpResponseRedirect

# Список активних голосувань
class VoteListView(ListView):
    model = Vote
    template_name = 'voting/vote_list.html'
    context_object_name = 'votes'

    def get_queryset(self):
        return Vote.objects.filter(is_active=True)


# Деталі голосування, із перевіркою, чи голосував користувач
class VoteDetailView(DetailView):
    model = Vote
    template_name = 'voting/vote_detail.html'
    context_object_name = 'vote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_voted'] = UserVote.objects.filter(vote=self.object, user=self.request.user).exists()
        return context


# Створення голосувань (доступно лише для адмінів/модераторів)
class VoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vote
    fields = ['title', 'description', 'is_active']
    template_name = 'voting/vote_form.html'
    success_url = reverse_lazy('voting:vote_list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Голосування успішно створено!')
        return super().form_valid(form)


# Обробка голосування з підтримкою переголосування (видаляє попередній голос)
class VoteCastView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        option_id = request.POST.get('option')
        option = get_object_or_404(VoteOption, pk=option_id, vote=vote)
        
        # Видаляємо попередній голос (для переголосування)
        UserVote.objects.filter(vote=vote, user=request.user).delete()
        
        # Створюємо новий голос
        UserVote.objects.create(vote=vote, option=option, user=request.user)
        option.vote_count += 1
        option.save()
        messages.success(request, 'Ваш голос зараховано!')
        return HttpResponseRedirect(reverse_lazy('voting:vote_detail', kwargs={'pk': pk}))
