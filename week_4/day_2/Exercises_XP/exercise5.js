const epic = ['a', 'long', 'time', 'ago', 'in a', 'galaxy', 'far far', 'away'];

const singleString = epic.reduce((accumulator, currentValue) => accumulator + " " + currentValue);

console.log(singleString);
