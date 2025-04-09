from django.contrib import admin
from .models import Reminder, MoodEntry, TherapistAppointment, Therapist

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'type', 'student')
    list_filter = ('type', 'date')
    search_fields = ('title', 'description')

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('student', 'mood', 'created_at')
    list_filter = ('mood', 'created_at')

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'is_available')
    list_filter = ('specialization', 'is_available')
    search_fields = ('name', 'specialization')

@admin.register(TherapistAppointment)
class TherapistAppointmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'therapist', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
