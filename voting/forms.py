from django import forms
from django.forms import inlineformset_factory
from .models import Vote, VoteOption

# Форма для створення нових голосувань
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Створюємо набір форм (formset) для моделі VoteOption, пов’язаної з Vote через ForeignKey.
# Formset дозволяє створювати або редагувати кілька екземплярів VoteOption для одного екземпляра Vote одночасно
VoteOptionFormSet = inlineformset_factory(
    Vote,                   # Батьківська модель, до якої прив’язані форми (одне голосування)
    VoteOption,             # Дочірня модель, для якої створюються форми (варіанти відповідей)
    fields=['text'],
    extra=3,                # кількість порожніх форм, які відображаються за замовчуванням у шаблоні (3 порожні поля для варіантів відповідей)
    can_delete=False,
    widgets={'text': forms.TextInput(attrs={'class': 'form-control'})},
)


# Кастомний клас formset, який успадковується від автоматично згенерованого VoteOptionFormSet.
# Це дозволяє додати власну логіку валідації, не змінюючи базовий formset
# Кастомна валідація гарантує, що користувач додасть щонайменше два варіанти відповідей, 
# інакше форма не пройде валідацію, і помилка відобразиться в шаблоні
class VoteOptionFormSet(VoteOptionFormSet):
    # Перевизначаємо метод, який викликається під час валідації formset для перевірки даних на рівні набору форм
    def clean(self):
        super().clean()
        if self.is_valid():
            # створюємо список форм, у яких поле text заповнене (не порожнє)
            filled_forms = [form for form in self.forms if form.cleaned_data.get('text')]
            if len(filled_forms) < 2:
                raise forms.ValidationError('Потрібно щонайменше два варіанти відповідей.')