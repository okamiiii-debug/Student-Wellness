document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    const circle = document.querySelector('.breathing-circle');
    const timerEl = document.getElementById('timer');
    const instructionEl = document.getElementById('instruction');
    const progressBar = document.getElementById('progress-bar');
    const exerciseComplete = document.getElementById('exercise-complete');
    
    let timer;
    let seconds = 60; // 1 minute exercise
    let breathingPhase = 'inhale'; // Can be 'inhale' or 'exhale'
    let isRunning = false;
    
    // Update UI
    function updateTimer() {
        timerEl.textContent = seconds;
        
        // Update progress bar
        const progress = (60 - seconds) / 60 * 100;
        progressBar.style.width = `${progress}%`;
        
        // Check if exercise is complete
        if (seconds <= 0) {
            clearInterval(timer);
            completeExercise();
        }
    }
    
    // Switch breathing phase
    function switchBreathingPhase() {
        if (breathingPhase === 'inhale') {
            breathingPhase = 'exhale';
            instructionEl.textContent = 'Breathe out';
            circle.classList.remove('inhale');
            circle.classList.add('exhale');
        } else {
            breathingPhase = 'inhale';
            instructionEl.textContent = 'Breathe in';
            circle.classList.remove('exhale');
            circle.classList.add('inhale');
        }
    }
    
    // Start exercise
    function startExercise() {
        if (isRunning) return;
        
        isRunning = true;
        startBtn.disabled = true;
        resetBtn.disabled = false;
        
        // Initial phase
        breathingPhase = 'inhale';
        instructionEl.textContent = 'Breathe in';
        circle.classList.add('inhale');
        
        // Start timer
        timer = setInterval(() => {
            seconds--;
            updateTimer();
            
            // Switch breathing phase every 4 seconds
            if (seconds % 4 === 0) {
                switchBreathingPhase();
            }
        }, 1000);
    }
    
    // Reset exercise
    function resetExercise() {
        clearInterval(timer);
        seconds = 60;
        isRunning = false;
        breathingPhase = 'inhale';
        
        // Reset UI
        instructionEl.textContent = 'Breathe in';
        timerEl.textContent = seconds;
        progressBar.style.width = '0%';
        circle.classList.remove('inhale', 'exhale');
        
        // Enable/disable buttons
        startBtn.disabled = false;
        resetBtn.disabled = true;
        
        // Hide completion message
        exerciseComplete.classList.add('d-none');
    }
    
    // Complete exercise
    function completeExercise() {
        isRunning = false;
        
        // Reset circle
        circle.classList.remove('inhale', 'exhale');
        
        // Show completion message
        exerciseComplete.classList.remove('d-none');
        
        // Enable reset button, disable start button
        startBtn.disabled = true;
        resetBtn.disabled = false;
    }
    
    // Event listeners
    startBtn.addEventListener('click', startExercise);
    resetBtn.addEventListener('click', resetExercise);
});
