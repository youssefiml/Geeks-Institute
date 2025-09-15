const family = {
    father: "Mohammed",
    mother: "Fatima",
    son: "Amine",
    daughter: "Amina"
};

for (let key in family) {
    console.log(`Key: ${key}`);
}

for (let value in family) {
    console.log(`Value: ${family[value]}`);
}