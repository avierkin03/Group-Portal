from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Material
from .forms import MaterialForm

# Список матеріалів
class MaterialListView(ListView):
    model = Material
    context_object_name = 'materials'
    template_name = 'materials/material_list.html'


# Додавання нового матеріалу
class MaterialCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/material_form.html'
    success_url = reverse_lazy('materials:material-list')

    # permission_required = 'materials.add_material'
    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Оновлення існуючого матеріалу
class MaterialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/material_form.html'
    success_url = reverse_lazy('materials:material-list')
    # permission_required = 'materials.change_material'

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']


# Видалення існуючого матеріалу
class MaterialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Material
    template_name = 'materials/material_delete_confirmation.html'
    success_url = reverse_lazy('materials:material-list')
    # permission_required = 'materials.delete_material'

    def test_func(self):
        return self.request.user.profile.role in ['admin', 'moderator']