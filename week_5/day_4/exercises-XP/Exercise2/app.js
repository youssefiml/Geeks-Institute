import people from './data.js';

function AverageAge(persons) {
    let totalAge = 0;

    for (const person of people) {
        totalAge += person.age;
    }

    const averageAge = totalAge / persons.length;

    console.log(`The average age is: ${averageAge}`);
}

AverageAge(people);