const colors = document.querySelectorAll('.color');
const grid = document.getElementById('grid');
let selectedColor = 'black';
let isDrawing = false;

for (let i = 0; i < 16 * 16; i++) {
  const square = document.createElement('div');
  square.classList.add('square');
  grid.appendChild(square);
}

colors.forEach(color => {
  color.addEventListener('click', () => {
    selectedColor = color.style.backgroundColor;
  });
});

grid.addEventListener('mousedown', () => isDrawing = true);
grid.addEventListener('mouseup', () => isDrawing = false);

const squares = document.querySelectorAll('.square');
squares.forEach(square => {
  square.addEventListener('mouseover', () => {
    if (isDrawing) square.style.backgroundColor = selectedColor;
  });
  square.addEventListener('mousedown', () => {
    square.style.backgroundColor = selectedColor;
  });
});
