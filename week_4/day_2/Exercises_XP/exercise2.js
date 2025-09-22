const colors = ["Blue", "Green", "Red", "Orange", "Violet", "Indigo", "Yellow"];
const ordinal = ["th","st","nd","rd"];

colors.forEach((color, index) => {
  const position = index + 1;

  const suffix = (position === 1) ? ordinal[1] :
                 (position === 2) ? ordinal[2] :
                 (position === 3) ? ordinal[3] :
                 ordinal[0];

  console.log(`${position}${suffix} choice is ${color}.`);
});
