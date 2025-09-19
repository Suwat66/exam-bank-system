document.addEventListener('DOMContentLoaded', function() {
    console.log("Exam Bank System JS Initialized");

    // Example Chart.js for Admin Dashboard
    const ctx = document.getElementById('usageChart');
    if (ctx) {
        // This data should be passed from the Django view in a real application
        const dummyLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        const dummyData = [120, 190, 30, 50, 25, 30];

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dummyLabels,
                datasets: [{
                    label: 'User Activity',
                    data: dummyData,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});