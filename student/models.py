from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Reminder(models.Model):
    TYPE_CHOICES = [
        ('test', 'Test'),
        ('assignment', 'Assignment'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_today(self):
        """Check if reminder is for today"""
        now = timezone.now()
        return self.date.date() == now.date()
    
    @property
    def is_past(self):
        """Check if reminder has passed"""
        return self.date < timezone.now()


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('calm', 'Calm'),
        ('neutral', 'Neutral'),
        ('anxious', 'Anxious'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Mood entries'
    
    def __str__(self):
        return f"{self.student.username} - {self.mood} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def is_negative(self):
        """Check if this is a negative mood"""
        return self.mood in ['anxious', 'sad', 'angry']


class Therapist(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class TherapistAppointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.therapist.name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
