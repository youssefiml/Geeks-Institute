const lodash = require('lodash');
const math = require('./math');

const num1 = lodash.random(1, 100);
const num2 = lodash.random(1, 100);

const sum = math.add(num1, num2);
const product = math.multiply(num1, num2);

console.log(`Sum: ${sum}`);
console.log(`Multiple: ${product}`);