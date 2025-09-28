const API_KEY = 'hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My';
const query = 'sun';
const limit = 10;
const offset = 2;
const url = `https://api.giphy.com/v1/gifs/search?api_key=${API_KEY}&q=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}&rating=g&lang=en`;

async function fetchSunGifs() {
  try {
    const response = await fetch(url);

    // check HTTP status
    if (!response.ok) {
      throw new Error(`Network response was not ok (status: ${response.status} ${response.statusText})`);
    }

    const json = await response.json();
    console.log(json);
  } catch (error) {
    console.error('Fetch failed:', error);
  }
}

fetchSunGifs();