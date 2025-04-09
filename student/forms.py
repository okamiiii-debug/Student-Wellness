from django import forms
from .models import Reminder, MoodEntry, TherapistAppointment
from django.utils import timezone

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date', 'type']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("You cannot set reminders for the past.")
        return date


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes about how you feel...'}),
        }


class TherapistAppointmentForm(forms.ModelForm):
    class Meta:
        model = TherapistAppointment
        fields = ['appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Briefly describe why you want to meet with the therapist...'}),
        }
    
    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date and date < timezone.now():
            raise forms.ValidationError("You cannot schedule appointments in the past.")
        return date
