document.addEventListener('DOMContentLoaded', () => {
    // Load Dashboard Stats
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error loading stats:", data.error);
                document.getElementById('total-samples').textContent = "Error loading data";
                return;
            }
            
            // Animate number counter
            const target = data.totalSamples;
            const counterElement = document.getElementById('total-samples');
            let current = 0;
            const duration = 1500;
            const stepTime = 20;
            const steps = duration / stepTime;
            const increment = target / steps;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counterElement.textContent = Math.floor(current).toLocaleString();
            }, stepTime);
            
            // Plot Chart
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            const labelsMap = {
                'Positive': 'Positive',
                'Negative': 'Negative',
                'Neutral': 'Neutral'
            };
            
            const dist = data.labelDistribution;
            const positive = dist['Positive'] || dist['positive'] || dist['2'] || 0;
            const neutral = dist['Neutral'] || dist['neutral'] || dist['1'] || 0;
            const negative = dist['Negative'] || dist['negative'] || dist['0'] || 0;
            
            // Modern colors inspired by our CSS theme
            Chart.defaults.font.family = "'Cairo', sans-serif";
            Chart.defaults.color = '#94a3b8';
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: [labelsMap['Positive'], labelsMap['Neutral'], labelsMap['Negative']],
                    datasets: [{
                        data: [positive, neutral, negative],
                        backgroundColor: [
                            'rgba(16, 185, 129, 0.8)', // Emerald
                            'rgba(245, 158, 11, 0.8)', // Amber
                            'rgba(239, 68, 68, 0.8)'   // Red
                        ],
                        borderColor: [
                            '#10b981',
                            '#f59e0b',
                            '#ef4444'
                        ],
                        borderWidth: 2,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '65%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: {
                                    size: 14,
                                    weight: '600'
                                },
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(15, 23, 42, 0.9)',
                            titleFont: { size: 14, family: "'Cairo', sans-serif" },
                            bodyFont: { size: 14, family: "'Cairo', sans-serif" },
                            padding: 12,
                            borderColor: 'rgba(255,255,255,0.1)',
                            borderWidth: 1,
                            cornerRadius: 8
                        }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    }
                }
            });
        })
        .catch(err => {
            console.error("Fetch error:", err);
            document.getElementById('total-samples').textContent = "Loading..."; // Keep default if file not present during dev
        });

    // Handle Prediction
    const btn = document.getElementById('analyze-btn');
    const input = document.getElementById('text-input');
    const resultBox = document.getElementById('result-box');
    const predLabel = document.getElementById('pred-label');
    const predScore = document.getElementById('pred-score');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.getElementById('loading-spinner');

    btn.addEventListener('click', () => {
        const text = input.value.trim();
        if (!text) {
            input.focus();
            return;
        }

        btn.disabled = true;
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('hidden');
        resultBox.classList.add('hidden');

        fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        })
        .then(response => response.json())
        .then(data => {
            btn.disabled = false;
            btnText.textContent = 'Analyze Sentiment';
            spinner.classList.add('hidden');
            
            if (data.error) {
                alert("Error occurred: " + data.error);
                return;
            }

            resultBox.classList.remove('hidden');
            
            let labelClean = data.sentiment.toLowerCase();
            let labelClass = 'neutral';
            let labelText = 'Neutral';
            
            if (labelClean.includes('positive')) {
                labelClass = 'positive';
                labelText = 'Positive';
            } else if (labelClean.includes('negative')) {
                labelClass = 'negative';
                labelText = 'Negative';
            }

            predLabel.textContent = labelText + (data.sentiment !== 'Model Unavailable' ? ` (${data.sentiment})` : '');
            predLabel.className = `badge ${labelClass}`; // replace classes
            predScore.textContent = `Confidence: ${(data.score * 100).toFixed(1)}%`;
        })
        .catch(err => {
            console.error(err);
            btn.disabled = false;
            btnText.textContent = 'Analyze Sentiment';
            spinner.classList.add('hidden');
            alert("Failed to connect to server.");
        });
    });
});
