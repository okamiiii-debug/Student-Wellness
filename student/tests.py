from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Reminder, MoodEntry, Therapist, TherapistAppointment
from django.utils import timezone
import datetime

class ReminderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reminder = Reminder.objects.create(
            student=self.user,
            title='Test Reminder',
            description='This is a test',
            date=timezone.now() + datetime.timedelta(days=1),
            type='test'
        )
        
    def test_reminder_creation(self):
        self.assertEqual(self.reminder.title, 'Test Reminder')
        self.assertEqual(self.reminder.type, 'test')
        
    def test_is_today_method(self):
        self.reminder.date = timezone.now()
        self.reminder.save()
        self.assertTrue(self.reminder.is_today)
        
    def test_str_method(self):
        self.assertEqual(str(self.reminder), 'Test Reminder')


class MoodEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.mood_entry = MoodEntry.objects.create(
            student=self.user,
            mood='happy',
            notes='Feeling great today'
        )
        
    def test_mood_entry_creation(self):
        self.assertEqual(self.mood_entry.mood, 'happy')
        
    def test_is_negative_method(self):
        self.assertFalse(self.mood_entry.is_negative)
        self.mood_entry.mood = 'sad'
        self.mood_entry.save()
        self.assertTrue(self.mood_entry.is_negative)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
        
    def test_dashboard_view_when_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
