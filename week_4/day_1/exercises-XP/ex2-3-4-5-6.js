// Exercise 2:
const winBattle = () => true;
let experiencePoints = winBattle() ? 10 : 1;
console.log(experiencePoints);

//Exercise 3:
const isString = (value) => {
    return typeof value === 'string';
};
console.log(isString('hello'));
console.log(isString(2)); 

//Exercise 4:
const sum = (a, b) => a + b;
console.log(sum(3, 5));

//Exercise 5:
function kgtograms(weight) {
    return weight * 1000;
}
const kgtograms = function (weight) {
    return weight * 1000;
};
const kgtograms = (weight) => weight * 1000;
console.log(kgtograms(5));

//Exercise 6:
(function(numchildern,partnersname,geographiclocation,jobtitle){
    console.log(`You will be a ${jobtitle} in ${geographiclocation}, and married to ${partnersname} with ${numchildern} kids.`);
})(2,"Alice","New York","Engineer");