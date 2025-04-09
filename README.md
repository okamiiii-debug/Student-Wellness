# Student-Wellness
HCI Module Project 2025

A Django-based student wellness application with features to help students manage stress, track mood, and access mental health resources.

## Features

- **Calendar Reminders**: Set reminders for tests, assignments, and other important events
- **Mood Tracking**: Log daily mood with a visual weekly mood graph
- **Breathing Exercises**: Guided 1-minute breathing sessions to reduce stress
- **Therapist Booking**: Schedule appointments with mental health professionals

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/student-wellness-app.git
   cd student-wellness-app
   ```
2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

## Technologies Used

- Django 5.2
- Bootstrap 5
- FullCalendar 5.11
- Chart.js 3.9
- SQLite (default database)

## Screenshots

[Add screenshots here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.