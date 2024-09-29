let latencyChart;
let ctx;  // Declare ctx for Chart.js context

// Fetch weather data from the server
function fetchWeatherData() {
    fetch("{% url 'ajax_get_data' %}")
        .then(response => response.json())
        .then(data => {
            // Debugging: Check the received data in the console
            console.log('Weather data:', data);

            // Update elements with fetched data
            updateTemperature(data.temperature);
            document.getElementById('current-location').textContent = data.location;
            document.getElementById('weather-icon').src = data.icon_url;
            document.getElementById('weather-description').textContent = data.weather;
            document.getElementById('current-wifi').textContent = data.wifi_ssid || 'Not available';
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById('current-location').textContent = 'Error fetching data';
        });
}

// Function to update the temperature display
function updateTemperature(temp) {
    const temperatureValue = document.getElementById('temperature-value');
    temperatureValue.textContent = temp ? `${temp}°C` : 'N/A';
}

// Fetch network latency data and update the chart
function fetchLatencyData() {
    fetch("{% url 'get_latency_data' %}")  // Ensure this URL points to the correct view
        .then(response => response.json())
        .then(data => {
            console.log('Latency data:', data);
            if (data.latency && data.latency.length > 0) {
                updateLatencyChart(data.latency);
            } else {
                console.warn('No latency data received.');
            }
        })
        .catch(error => console.error('Error fetching latency data:', error));
}

// Function to update the Chart.js network latency graph
function updateLatencyChart(latencyValues) {
    // Destroy existing chart if it exists to avoid overlap
    if (latencyChart) {
        latencyChart.destroy();
    }

    // Recreate the Chart.js instance
    latencyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: latencyValues.length }, (_, i) => `Sample ${i + 1}`),
            datasets: [{
                label: 'Network Latency (ms)',
                data: latencyValues,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Light background color
                borderColor: 'rgba(75, 192, 192, 1)',  // Line color
                borderWidth: 2,
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 1,
                pointRadius: 3,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: { color: '#fff' },  // White color for X-axis labels
                    grid: { color: 'rgba(255, 255, 255, 0.2)' }  // Light grid lines
                },
                y: {
                    ticks: { color: '#fff' },  // White color for Y-axis labels
                    grid: { color: 'rgba(255, 255, 255, 0.2)' }  // Light grid lines
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#fff' }  // White color for legend labels
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',  // Dark background for tooltips
                    titleColor: '#fff',  // White color for tooltip title
                    bodyColor: '#fff'  // White color for tooltip body
                }
            }
        }
    });
}

// Function to handle user logout
function logoutUser() {
    window.location.href = "/login";
}

// Run these functions once the page loads
window.onload = function() {
    ctx = document.getElementById('latencyChart').getContext('2d');  // Initialize ctx
    fetchWeatherData();  // Fetch weather data when the page loads
    fetchLatencyData();  // Fetch latency data when the page loads

    // Refresh weather data every 30 minutes
    setInterval(fetchWeatherData, 1800000);  // 30 minutes

    // Refresh latency data every 5 seconds
    setInterval(fetchLatencyData, 5000);  // 5 seconds
};
