const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");
const info = document.getElementById("info");
const btn = document.getElementById("findsomeone");

function initCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function createStars() {
  const stars = [];
  for (let i = 0; i < 200; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2,
      speed: Math.random() * 1 + 0.5
    });
  }
  return stars;
}

function animateStars(stars) {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  
  stars.forEach(star => {
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
    ctx.fill();
    star.y += star.speed;
    if (star.y > canvas.height) {
      star.y = 0;
      star.x = Math.random() * canvas.width;
    }
  });
  requestAnimationFrame(() => animateStars(stars));
}

function showLoading() {
  info.innerHTML = `<p><i class="fas fa-spinner fa-spin"></i> Loading...</p>`;
}

function showError() {
  info.innerHTML = "<p>Oh no! That person is not available.</p>";
}

function displayCharacterInfo(character, homeworldName) {
  info.innerHTML = `
    <h2>${character.name}</h2>
    <p><strong>Height:</strong> ${character.height}</p>
    <p><strong>Gender:</strong> ${character.gender}</p>
    <p><strong>Birth Year:</strong> ${character.birth_year}</p>
    <p><strong>Homeworld:</strong> ${homeworldName}</p>
  `;
}

async function fetchHomeworld(homeworldUrl) {
  const response = await fetch(homeworldUrl);
  const data = await response.json();
  return data.result.properties.name;
}

async function fetchRandomCharacter() {
  try {
    showLoading();
    
    const id = Math.floor(Math.random() * 83) + 1;
    const response = await fetch(`https://www.swapi.tech/api/people/${id}`);
    const data = await response.json();
    const character = data.result.properties;
    
    const homeworldName = await fetchHomeworld(character.homeworld);
    displayCharacterInfo(character, homeworldName);
    
  } catch (error) {
    showError();
  }
}

function init() {
  initCanvas();
  const stars = createStars();
  animateStars(stars);
  
  btn.addEventListener("click", fetchRandomCharacter);
  
  window.addEventListener("resize", () => {
    initCanvas();
  });
}

init();