// PART 1:
console.log([2] === [2]); //False
console.log({} === {}); //False


// PART 2:
const object1 = { number: 5 };
const object2 = object1;
const object3 = object2;
const object4 = { number: 5 };

object1.number = 4;

console.log(object2.number);
console.log(object3.number);
console.log(object4.number);


// PART 3:
class Animal {
  constructor(name, type, color) {
    this.name = name;
    this.type = type;
    this.color = color;
  }
}

class Mammal extends Animal {
    sound(animalSound) {
      return `${animalSound} I'm a ${this.type}, named ${this.name} and I'm ${this.color}`;
    }
}
const farmerCow = new Mammal('Lily', 'cow', 'brown and white');

console.log(farmerCow.sound('Moooo'));