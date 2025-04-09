function initializeMoodChart() {
    const ctx = document.getElementById('moodChart');
    if (!ctx) return;
    
    // Fetch mood data from the server
    fetch('/mood/graph-data/')
        .then(response => response.json())
        .then(data => {
            createMoodChart(ctx, data.mood_data);
        })
        .catch(error => {
            console.error('Error fetching mood data:', error);
        });
}

function createMoodChart(ctx, moodData) {
    // Define colors for each mood type
    const colors = {
        'happy': '#4CAF50',  // Green
        'calm': '#2196F3',   // Blue
        'neutral': '#9E9E9E', // Gray
        'anxious': '#FFC107', // Amber
        'sad': '#2196F3',    // Blue (slightly different shade)
        'angry': '#F44336'   // Red
    };
    
    // Create mood datasets
    const datasets = [];
    
    // Get all unique dates
    const dates = moodData.map(item => item.date);
    
    // Create a dataset for each mood type
    ['happy', 'calm', 'neutral', 'anxious', 'sad', 'angry'].forEach(mood => {
        datasets.push({
            label: mood.charAt(0).toUpperCase() + mood.slice(1),
            data: moodData.map(item => item[mood]),
            backgroundColor: colors[mood],
            borderColor: colors[mood],
            borderWidth: 1
        });
    });
    
    // Create chart
    const moodChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false,
                    text: 'Mood Tracking'
                }
            },
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}
