function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;
    
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek'
        },
        events: '/api/reminders/',
        eventClick: function(info) {
            // Open modal to edit event
            const modal = new bootstrap.Modal(document.getElementById('addReminderModal'));
            
            // Fill in the form with event data
            document.getElementById('title').value = info.event.title;
            document.getElementById('date').value = formatDateForInput(info.event.start);
            document.getElementById('type').value = info.event.extendedProps.type || 'other';
            document.getElementById('description').value = info.event.extendedProps.description || '';
            
            // Change form action to edit endpoint
            const form = document.querySelector('#addReminderModal form');
            form.action = `/reminder/edit/${info.event.id}/`;
            
            // Change modal title
            document.getElementById('addReminderModalLabel').textContent = 'Edit Reminder';
            
            modal.show();
        },
        dateClick: function(info) {
            // Open modal to add new event on the clicked date
            const modal = new bootstrap.Modal(document.getElementById('addReminderModal'));
            
            // Clear form
            document.getElementById('title').value = '';
            document.getElementById('date').value = formatDateForInput(info.date);
            document.getElementById('type').value = 'other';
            document.getElementById('description').value = '';
            
            // Change form action to create endpoint
            const form = document.querySelector('#addReminderModal form');
            form.action = '/reminder/create/';
            
            // Change modal title
            document.getElementById('addReminderModalLabel').textContent = 'Add New Reminder';
            
            modal.show();
        },
        eventClassNames: function(arg) {
            // Add classes based on event type
            return ['reminder-' + arg.event.extendedProps.type];
        }
    });
    
    calendar.render();
    
    // Function to format date for datetime-local input
    function formatDateForInput(date) {
        const d = new Date(date);
        // Format: YYYY-MM-DDThh:mm
        return d.getFullYear() + '-' + 
               String(d.getMonth() + 1).padStart(2, '0') + '-' + 
               String(d.getDate()).padStart(2, '0') + 'T' + 
               String(d.getHours()).padStart(2, '0') + ':' + 
               String(d.getMinutes()).padStart(2, '0');
    }
}
