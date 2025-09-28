const API_KEY = 'hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My';
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const gifsContainer = document.getElementById('gifsContainer');
const deleteAllBtn = document.getElementById('deleteAllBtn');
searchForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
        await fetchRandomGif(query);
        searchInput.value = '';
    }
});
async function fetchRandomGif(query) {
    try {
        const response = await fetch(`https://api.giphy.com/v1/gifs/random?api_key=${API_KEY}&tag=${query}`);
        const data = await response.json();
        
        if (data.data && data.data.images) {
            displayGif(data.data);
        }
    } catch (error) {
        console.error('Error fetching GIF:', error);
    }
}
function displayGif(gif) {
    const gifDiv = document.createElement('div');
    gifDiv.innerHTML = `
        <img src="${gif.images.fixed_height.url}" alt="GIF">
        <button onclick="deleteGif(this)">DELETE</button>
    `;
    gifsContainer.appendChild(gifDiv);
}
function deleteGif(button) {
    button.parentElement.remove();
}
deleteAllBtn.addEventListener('click', function() {
    gifsContainer.innerHTML = '';
});