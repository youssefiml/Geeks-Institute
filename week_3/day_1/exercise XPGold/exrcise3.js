let age = [20, 5, 12, 43, 91, 55];
let sum = 0;
for (let i of age) {
    sum += i;
}
console.log("Sum of ages:", sum);

let max = age[0];
for (let i = 1; i < age.length; i++) {
    if (age[i] > max) {
        max = age[i];
    }
}
console.log("Highest age:", max);