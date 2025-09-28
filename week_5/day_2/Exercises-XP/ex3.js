async function getStarship() {
  const url = "https://www.swapi.tech/api/starships/9/";

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log(data.result);

  } catch (error) {
    console.error("Fetch failed:", error);
  }
}

getStarship();
