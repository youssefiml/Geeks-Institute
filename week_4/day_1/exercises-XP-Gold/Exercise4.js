// Analyse:
// curriedSum(5) returns a function that adds 5 to its argument.
// add5 is now a function: b => 5 + b
// Calling add5(12) adds 5 + 12
const curriedSum2 = (a) => (b) => a + b;
const add5 = curriedSum2(5);

console.log(add5(12)); // 17
