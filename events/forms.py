from django import forms
from .models import Event

# Форма для створення/редагування подій
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Форма для фільтрації подій
class EventFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Дата",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )