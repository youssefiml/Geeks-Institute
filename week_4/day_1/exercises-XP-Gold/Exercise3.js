// Analyse:
// curriedSum is a curried function: it takes 'a' and returns a function taking 'b'.
// curriedSum(30) returns a function b => 30 + b
// curriedSum(30)(1) applies 1 to the inner function, resulting in 30 + 1
const curriedSum = (a) => (b) => a + b;

console.log(curriedSum(30)(1)); // 31
