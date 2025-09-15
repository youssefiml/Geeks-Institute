// Part I - Review about arrays

const people = ["Greg", "Mary", "Devon", "James"];

people.shift("Greg");

people[people.indexOf("James")] = "Jason";

people.push("Youssef");

console.log(people.indexOf("Mary"));

const peopleCopy = people.slice();

console.log(peopleCopy.indexOf("Foo"));

let last = people.length - 1;
console.log(people[last]);

// Part II - Loops

for (let i = 0; i < people.length; i++) {
  console.log(people[i]);
}

for (let i = 0; i < people.length; i++) {
  if (people[i] === "Jason") {
    break;
  }
}