const data = [
  { name: 'Butters', age: 3, type: 'dog' },
  { name: 'Cuty', age: 5, type: 'rabbit' },
  { name: 'Lizzy', age: 6, type: 'dog' },
  { name: 'Red', age: 1, type: 'cat' },
  { name: 'Joey', age: 3, type: 'dog' },
  { name: 'Rex', age: 10, type: 'dog' },
];

let totalHumanYears = 0;

for (let animal of data) {
  if (animal.type === 'dog') {
    totalHumanYears += animal.age * 7;
  }
}

console.log(totalHumanYears);

const totalHumanYearsReduce = data.reduce((sum, animal) => {
  return animal.type === 'dog' ? sum + animal.age * 7 : sum;
}, 0);

console.log(totalHumanYearsReduce);
