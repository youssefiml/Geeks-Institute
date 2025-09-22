// 1
const fruits = ["apple", "orange"];
const vegetables = ["carrot", "potato"];

const result = ['bread', ...vegetables, 'chicken', ...fruits];
console.log("Output 1:", result);


// 2
const country = "USA";
console.log("Output 2:", [...country]);


// Bonus
let newArray = [...[,,]];
console.log("Bonus Output:", newArray);
