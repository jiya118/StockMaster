// Dashboard specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    loadLowStockAlerts();
    setupRealTimeUpdates();
});

async function loadLowStockAlerts() {
    try {
        const response = await fetch('/api/low-stock-alerts');
        const alerts = await response.json();
        
        if (alerts.length > 0) {
            showLowStockAlert(alerts);
        }
    } catch (error) {
        console.error('Failed to load low stock alerts:', error);
    }
}

function showLowStockAlert(alerts) {
    const alertContainer = document.createElement('div');
    alertContainer.className = 'alert alert-error';
    alertContainer.innerHTML = `
        <strong>Low Stock Alert!</strong>
        <div style="margin-top: 10px;">
            ${alerts.map(alert => `
                <div>${alert.name} (${alert.sku}) - ${alert.quantity} left in ${alert.warehouse_name}</div>
            `).join('')}
        </div>
    `;
    
    // Insert at the top of main content
    const mainContent = document.querySelector('.main-content');
    const firstChild = mainContent.firstChild;
    mainContent.insertBefore(alertContainer, firstChild);
}

function setupRealTimeUpdates() {
    // Simulate real-time updates (in a real app, you'd use WebSockets)
    setInterval(() => {
        updateKPI('pending-receipts');
        updateKPI('pending-deliveries');
    }, 30000); // Update every 30 seconds
}

async function updateKPI(kpiType) {
    try {
        // This would be an API endpoint that returns updated KPI data
        // For now, we'll just simulate an update
        const kpiElement = document.querySelector(`[data-kpi="${kpiType}"]`);
        if (kpiElement) {
            const currentValue = parseInt(kpiElement.textContent);
            const change = Math.random() > 0.5 ? 1 : -1;
            kpiElement.textContent = Math.max(0, currentValue + change);
        }
    } catch (error) {
        console.error('Failed to update KPI:', error);
    }
}

// Chart initialization (if you add charts later)
function initCharts() {
    // Example using Chart.js (you'll need to include Chart.js in your project)
    const ctx = document.getElementById('inventoryChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Stock Movements',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: '#C9B59C'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
}