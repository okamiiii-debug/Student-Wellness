from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Dashboard and main views
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Reminder management
    path('reminder/create/', views.create_reminder, name='create_reminder'),
    path('reminder/edit/<int:reminder_id>/', views.edit_reminder, name='edit_reminder'),
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('reminders/today/', views.today_reminders, name='today_reminders'),
    
    # Mood tracking
    path('mood/log/', views.log_mood, name='log_mood'),
    path('mood/history/', views.mood_history, name='mood_history'),
    path('mood/graph-data/', views.mood_graph_data, name='mood_graph_data'),
    
    # Breathing exercises
    path('breathing-exercise/', views.breathing_exercise, name='breathing_exercise'),
    
    # Therapist booking
    path('therapist/list/', views.therapist_list, name='therapist_list'),
    path('therapist/book/<int:therapist_id>/', views.book_therapist, name='book_therapist'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    
    # API endpoints
    path('api/reminders/', views.reminders_api, name='reminders_api'),
]
