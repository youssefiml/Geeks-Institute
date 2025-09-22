const colors = ["Blue", "Green", "Red", "Orange", "Violet", "Indigo", "Yellow"];

colors.forEach((color, index) => {
  console.log(`${index + 1}# choice is ${color}.`);
});

colors.some(color => color === "Violet")
  ? console.log("Yeah")
  : console.log("No...");
