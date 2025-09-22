class Dog {
  constructor(name) {
    this.name = name;
  }
};

class Labrador extends Dog {
  constructor(name, size) {
    super(name);  
    this.size = size;
  }
};

// Example test
const lab = new Labrador('Youssef', 'Medium');
console.log(lab.name);
console.log(lab.size);