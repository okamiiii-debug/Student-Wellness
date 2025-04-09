# Setup Guide for Development

This guide outlines the steps needed to set up this project in a local development environment.

## Dependencies

- Python 3.11 or higher
- Django 5.2

## Setup Instructions

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Django:
   ```bash
   pip install django==5.2
   ```

3. Clone the repository (if you haven't already):
   ```bash
   git clone https://github.com/your-username/student-wellness-app.git
   cd student-wellness-app
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations student
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Adding Sample Data (Optional)

To add sample therapists to the application:

```python
# Run this in Django shell: python manage.py shell
from student.models import Therapist
Therapist.objects.create(
    name='Dr. Emily Johnson',
    specialization='Anxiety Management',
    description='Specializes in helping students manage anxiety and stress during exams and transitions.',
    is_available=True
)
Therapist.objects.create(
    name='Dr. Michael Chen',
    specialization='Depression & Mood Disorders',
    description='Focuses on evidence-based approaches to managing depression and improving emotional wellness.',
    is_available=True
)
Therapist.objects.create(
    name='Dr. Sarah Williams',
    specialization='Academic Stress',
    description='Helps students develop coping mechanisms for academic pressure and perfectionism.',
    is_available=True
)
```