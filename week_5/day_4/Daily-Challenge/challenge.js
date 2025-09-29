const { greet } = require('./greeting');
const { displayColorfulMessage } = require('./colorful-message');
const { readFileContent } = require('./read-file');

console.log('TASK 1: Greeting Module');
const greeting = greet('Developer');
console.log(greeting);
console.log();

console.log('TASK 2: Colorful Message with Chalk');
displayColorfulMessage();
console.log();

console.log('TASK 3: File Operations');
readFileContent();