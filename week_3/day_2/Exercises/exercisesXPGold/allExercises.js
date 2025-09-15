// Exercise 1: isBlank
function isBlank(str) {
    return str.trim() === '';
}

console.log("Exercise 1:");
console.log(isBlank(''));
console.log(isBlank('abc'));

// Exercise 2: abbrevName 
function abbrevName(name) {
    const [firstName, lastName] = name.split(" ");
    return `${firstName} ${lastName[0]}.`;
}

console.log("Exercise 2:");
console.log(abbrevName("Robin Singh"));

// Exercise 3: swapCase
function swapCase(str) {
    return str
        .split('')
        .map(char => char === char.toUpperCase() ? char.toLowerCase() : char.toUpperCase())
        .join('');
}

console.log("Exercise 3:");
console.log(swapCase('The Quick Brown Fox'));

// Exercise 4: isOmnipresent
function isOmnipresent(arr, val) {
    return arr.every(subArr => subArr.includes(val));
}

console.log("Exercise 4:");
console.log(isOmnipresent([[1, 1], [1, 3], [5, 1], [6, 1]], 1));
console.log(isOmnipresent([[1, 1], [1, 3], [5, 1], [6, 1]], 6));

// Exercise 5: Red Table
function colorDiagonal(tableId) {
    const table = document.getElementById(tableId);
    const rows = table.rows;
    for (let i = 0; i < rows.length; i++) {
        if (rows[i].cells[i]) {
            rows[i].cells[i].style.backgroundColor = 'red';
        }
    }
}