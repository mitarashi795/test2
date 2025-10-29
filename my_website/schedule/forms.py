# schedule/forms.py (新規作成)
from django import forms
from .models import Event

# schedule/forms.py

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
            # ★class属性を追加
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'flatpickr-datetime'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'flatpickr-datetime'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)