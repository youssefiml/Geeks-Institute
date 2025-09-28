const form = document.getElementById('sunriseForm');
const results = document.getElementById('results');
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const lat1 = document.getElementById('lat1').value;
    const lng1 = document.getElementById('lng1').value;
    const lat2 = document.getElementById('lat2').value;
    const lng2 = document.getElementById('lng2').value;
    
    results.innerHTML = 'Loading...';
    
    try {
        const promises = [
            fetchSunrise(lat1, lng1),
            fetchSunrise(lat2, lng2)
        ];
        
        const sunriseTimes = await Promise.all(promises);
        
        results.innerHTML = `
            <div class="city-result">
                <strong>City 1 (${lat1}, ${lng1}):</strong> Sunrise at ${sunriseTimes[0]}
            </div>
            <div class="city-result">
                <strong>City 2 (${lat2}, ${lng2}):</strong> Sunrise at ${sunriseTimes[1]}
            </div>
        `;
        
    } catch (error) {
        results.innerHTML = 'Error fetching sunrise times';
    }
});
async function fetchSunrise(lat, lng) {
    const response = await fetch(`https://api.sunrise-sunset.org/json?lat=${lat}&lng=${lng}&formatted=0`);
    const data = await response.json();
    
    if (data.status === 'OK') {
        const sunriseTime = new Date(data.results.sunrise);
        return sunriseTime.toLocaleTimeString();
    } else {
        throw new Error('Failed to fetch sunrise data');
    }
};