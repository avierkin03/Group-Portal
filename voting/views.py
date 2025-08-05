from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Vote, VoteOption, UserVote
from django.http import HttpResponseRedirect
from .forms import VoteForm, VoteOptionFormSet

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
    form_class = VoteForm
    template_name = 'voting/vote_form.html'
    success_url = reverse_lazy('voting:vote_list')

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = VoteOptionFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = VoteOptionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.instance.created_by = self.request.user
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Голосування та варіанти відповідей успішно створено!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Помилка: перевірте варіанти відповідей.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка: перевірте дані форми.')
        return self.render_to_response(self.get_context_data(form=form))
    

# Обробка голосування з підтримкою переголосування (видаляє попередній голос)
class VoteCastView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        option_id = request.POST.get('option')
        option = get_object_or_404(VoteOption, pk=option_id, vote=vote)
        
        vote_cast, created = UserVote.objects.get_or_create(
            user=request.user,
            vote=vote,
            defaults={'option': option}
        )
        
        if created:
            # Новий голос: збільшуємо vote_count для вибраного варіанту
            option.vote_count += 1
            option.save()
        else:
            # Переголосування: зменшуємо vote_count попереднього варіанту
            if vote_cast.option != option:
                vote_cast.option.vote_count -= 1
                vote_cast.option.save()
                # Збільшуємо vote_count для нового варіанту
                option.vote_count += 1
                option.save()
                # Оновлюємо вибір
                vote_cast.option = option
                vote_cast.save()
        
        messages.success(request, 'Ваш голос зараховано!')
        return redirect('voting:vote_detail', pk=vote.pk)
