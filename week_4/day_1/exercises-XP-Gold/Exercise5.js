// Analyse:
// compose(f, g) returns a function a => f(g(a))
// add5(10) = 15
// add1(15) = 16
// So compose(add1, add5)(10) = add1(add5(10)) = 16
const compose = (f, g) => (a) => f(g(a));
const add1 = (num) => num + 1;
const add5 = (num) => num + 5;

console.log(compose(add1, add5)(10)); // 16
