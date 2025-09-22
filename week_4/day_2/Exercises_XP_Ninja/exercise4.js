const letters = ['x', 'y', 'z', 'z'];

const count = {};

for (let letter of letters) {
  count[letter] = (count[letter] || 0) + 1;
}

console.log(count);

const countReduce = letters.reduce((acc, letter) => {
  acc[letter] = (acc[letter] || 0) + 1;
  return acc;
}, {});

console.log(countReduce);
