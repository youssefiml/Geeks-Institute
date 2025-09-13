
const person1 = {
    fullName: "Jack",
    mass: 88,
    height: 1.81,
    calcBMI: function () {
        return this.mass / (this.height ** 2);
    }
};
const person2 = {
    fullName: "Youssef",
    mass: 59,
    height: 1.69,
    calcBMI: function () {
        return this.mass / (this.height ** 2);
    }
};
function compareBMI(p1, p2) {
    const bmi1 = p1.calcBMI();
    const bmi2 = p2.calcBMI();
    if (bmi1 > bmi2) {
        console.log(`${p1.fullName} has a higher BMI: ${bmi1}`);
    } else if (bmi2 > bmi1) {
        console.log(`${p2.fullName} has a higher BMI: ${bmi2}`);
    } else {
        console.log(`${p1.fullName} and ${p2.fullName} have the same BMI: ${bmi1.toFixed(2)}`);
    }
}
compareBMI(person1, person2);
