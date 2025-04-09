from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Reminder, MoodEntry, Therapist, TherapistAppointment
from .forms import ReminderForm, MoodEntryForm, TherapistAppointmentForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

def index(request):
    """Redirect to dashboard if logged in, otherwise show landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')

def register(request):
    """Register new user"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get today's reminders
    today = timezone.now().date()
    today_reminders = Reminder.objects.filter(
        student=request.user,
        date__date=today
    ).order_by('date')
    
    # Get upcoming reminders (within 7 days)
    upcoming_reminders = Reminder.objects.filter(
        student=request.user,
        date__date__gt=today,
        date__date__lte=today + timedelta(days=7)
    ).order_by('date')
    
    # Get most recent mood entry
    try:
        latest_mood = MoodEntry.objects.filter(student=request.user).latest('created_at')
    except MoodEntry.DoesNotExist:
        latest_mood = None
        
    # Get weekly mood data
    week_ago = today - timedelta(days=7)
    weekly_moods = MoodEntry.objects.filter(
        student=request.user,
        created_at__date__gte=week_ago
    ).order_by('created_at')
    
    return render(request, 'dashboard.html', {
        'today_reminders': today_reminders,
        'upcoming_reminders': upcoming_reminders,
        'latest_mood': latest_mood,
        'weekly_moods': weekly_moods,
    })

@login_required
def create_reminder(request):
    """Create a new reminder"""
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.student = request.user
            reminder.save()
            return redirect('dashboard')
    else:
        form = ReminderForm()
    
    return render(request, 'dashboard.html', {'form': form})

@login_required
def edit_reminder(request, reminder_id):
    """Edit an existing reminder"""
    reminder = get_object_or_404(Reminder, id=reminder_id, student=request.user)
    
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ReminderForm(instance=reminder)
        
    return render(request, 'dashboard.html', {'form': form, 'editing': True})

@login_required
def delete_reminder(request, reminder_id):
    """Delete a reminder"""
    reminder = get_object_or_404(Reminder, id=reminder_id, student=request.user)
    
    if request.method == 'POST':
        reminder.delete()
        return redirect('dashboard')
        
    return render(request, 'dashboard.html', {'reminder': reminder, 'confirm_delete': True})

@login_required
def today_reminders(request):
    """Get today's reminders for AJAX requests"""
    today = timezone.now().date()
    reminders = Reminder.objects.filter(
        student=request.user,
        date__date=today
    ).order_by('date')
    
    reminders_list = [
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'time': r.date.strftime('%H:%M'),
            'type': r.type
        } 
        for r in reminders
    ]
    
    return JsonResponse({'reminders': reminders_list})

@login_required
def log_mood(request):
    """Log a new mood entry"""
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.student = request.user
            mood_entry.save()
            
            # If negative mood, redirect to breathing exercise
            if mood_entry.is_negative:
                return redirect('breathing_exercise')
            return redirect('dashboard')
    else:
        form = MoodEntryForm()
    
    return render(request, 'dashboard.html', {'mood_form': form})

@login_required
def mood_history(request):
    """View mood history"""
    moods = MoodEntry.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'moods': moods, 'show_history': True})

@login_required
def mood_graph_data(request):
    """Get mood data for the graph (AJAX endpoint)"""
    # Get the past 7 days of mood data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)  # 7 days total including today
    
    # Initialize result with all days
    result = {}
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        result[current_date.strftime('%Y-%m-%d')] = {
            'date': current_date.strftime('%a'),  # Abbreviated weekday name
            'happy': 0, 'calm': 0, 'neutral': 0, 
            'anxious': 0, 'sad': 0, 'angry': 0
        }
    
    # Get mood counts for each day
    mood_data = MoodEntry.objects.filter(
        student=request.user,
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).values('created_at__date', 'mood').annotate(count=Count('id'))
    
    # Populate the result
    for item in mood_data:
        date_str = item['created_at__date'].strftime('%Y-%m-%d')
        if date_str in result:
            result[date_str][item['mood']] = item['count']
    
    # Convert to list for easier consumption by Chart.js
    result_list = list(result.values())
    
    return JsonResponse({'mood_data': result_list})

@login_required
def breathing_exercise(request):
    """Breathing exercise page"""
    return render(request, 'breathing_exercise.html')

@login_required
def therapist_list(request):
    """List available therapists"""
    therapists = Therapist.objects.filter(is_available=True)
    return render(request, 'therapist_booking.html', {'therapists': therapists})

@login_required
def book_therapist(request, therapist_id):
    """Book a therapist appointment"""
    therapist = get_object_or_404(Therapist, id=therapist_id, is_available=True)
    
    if request.method == 'POST':
        form = TherapistAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = request.user
            appointment.therapist = therapist
            appointment.status = 'pending'
            appointment.save()
            return redirect('appointment_list')
    else:
        form = TherapistAppointmentForm()
    
    return render(request, 'therapist_booking.html', {
        'therapist': therapist,
        'form': form
    })

@login_required
def appointment_list(request):
    """View user's appointments"""
    appointments = TherapistAppointment.objects.filter(
        student=request.user
    ).order_by('-appointment_date')
    
    return render(request, 'therapist_booking.html', {
        'appointments': appointments,
        'show_appointments': True
    })

@csrf_exempt
@login_required
def reminders_api(request):
    """API endpoint for calendar reminders"""
    if request.method == 'GET':
        # Get reminders for calendar display
        start_str = request.GET.get('start')
        end_str = request.GET.get('end')
        
        if not start_str or not end_str:
            return JsonResponse({'error': 'Start and end dates are required'}, status=400)
            
        try:
            start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        reminders = Reminder.objects.filter(
            student=request.user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        events = [
            {
                'id': reminder.id,
                'title': reminder.title,
                'start': reminder.date.isoformat(),
                'end': (reminder.date + timedelta(hours=1)).isoformat(),
                'classNames': [f'reminder-type-{reminder.type}'],
                'extendedProps': {
                    'description': reminder.description,
                    'type': reminder.type
                }
            }
            for reminder in reminders
        ]
        
        return JsonResponse(events, safe=False)
        
    elif request.method == 'POST':
        # Create a new reminder
        try:
            data = json.loads(request.body)
            title = data.get('title')
            start = data.get('start')
            description = data.get('description', '')
            reminder_type = data.get('type', 'other')
            
            if not title or not start:
                return JsonResponse({'error': 'Title and start date are required'}, status=400)
                
            start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
            
            reminder = Reminder.objects.create(
                student=request.user,
                title=title,
                description=description,
                date=start_date,
                type=reminder_type
            )
            
            return JsonResponse({
                'id': reminder.id,
                'title': reminder.title,
                'start': reminder.date.isoformat(),
                'success': True
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'PUT':
        # Update an existing reminder
        try:
            data = json.loads(request.body)
            reminder_id = data.get('id')
            
            if not reminder_id:
                return JsonResponse({'error': 'Reminder ID is required'}, status=400)
                
            reminder = get_object_or_404(Reminder, id=reminder_id, student=request.user)
            
            if 'title' in data:
                reminder.title = data['title']
            if 'start' in data:
                reminder.date = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
            if 'description' in data:
                reminder.description = data['description']
            if 'type' in data:
                reminder.type = data['type']
                
            reminder.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        # Delete a reminder
        try:
            data = json.loads(request.body)
            reminder_id = data.get('id')
            
            if not reminder_id:
                return JsonResponse({'error': 'Reminder ID is required'}, status=400)
                
            reminder = get_object_or_404(Reminder, id=reminder_id, student=request.user)
            reminder.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
