// Analyse: 
// addTo is a function that returns another function.
// x is "remembered" inside the inner function y => x + y due to closure.
// addToTen stores the inner function with x = 10.
// Calling addToTen(3) adds 10 + 3.
const addTo = x => y => x + y;

const addToTen = addTo(10); // returns y => 10 + y

console.log(addToTen(3)); // 13
