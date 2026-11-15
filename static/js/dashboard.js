
const dataElement = document.getElementById("dashboard-data");

if (dataElement) {
    const dashboardData = JSON.parse(dataElement.textContent);

    // Daily spending line chart
    const dailyCanvas = document.getElementById("dailyChart");

    if (dailyCanvas) {
        new Chart(dailyCanvas, {
            type: "line",
            data: {
                labels: dashboardData.daily_labels,
                datasets: [{
                    label: "Spending (₹)",
                    data: dashboardData.daily_amounts,
                    borderColor: "#23865b",
                    backgroundColor: "rgba(35, 134, 91, 0.12)",
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: value => "₹" + value
                        }
                    }
                }
            }
        });
    }

    // Category doughnut chart
    const categoryCanvas = document.getElementById("categoryChart");

    if (categoryCanvas) {
        new Chart(categoryCanvas, {
            type: "doughnut",
            data: {
                labels: dashboardData.category_labels,
                datasets: [{
                    data: dashboardData.category_amounts,
                    backgroundColor: [
                        "#23865b",
                        "#80b89a",
                        "#b6d9c4",
                        "#e2b66d",
                        "#7797a6",
                        "#b7a2c9",
                        "#d98f83",
                        "#9ca3af",
                        "#d4c5a9"
                    ],
                    borderWidth: 2,
                    borderColor: "#ffffff"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }
}
