// ================= Exercise 1: Random Number and Even Numbers =================
function randomEvenNumbers() {
    const randomNum = Math.floor(Math.random() * 100) + 1;
    console.log("Random number:", randomNum);
    console.log("Even numbers from 0 to", randomNum, ":");
    for (let i = 0; i <= randomNum; i += 2) {
        console.log(i);
    }
}
randomEvenNumbers();

// ================= Exercise 2: Capitalized Letters =================
function capitalize(str) {
    const evenCaps = str.split('').map((ch, i) => i % 2 === 0 ? ch.toUpperCase() : ch).join('');
    const oddCaps = str.split('').map((ch, i) => i % 2 !== 0 ? ch.toUpperCase() : ch).join('');
    return [evenCaps, oddCaps];
}

console.log("Exercise 2:");
console.log(capitalize("abcdef")); // ['AbCdEf', 'aBcDeF']

// ================= Exercise 3: Is Palindrome =================
function isPalindrome(str) {
    const reversed = str.split('').reverse().join('');
    return str === reversed;
}

console.log("Exercise 3:");
console.log(isPalindrome("madam")); // true
console.log(isPalindrome("hello")); // false

// ================= Exercise 4: Biggest Number in Array =================
function biggestNumberInArray(arr) {
    const nums = arr.filter(el => typeof el === 'number');
    return nums.length > 0 ? Math.max(...nums) : 0;
}

console.log("Exercise 4:");
console.log(biggestNumberInArray([-1,0,3,100, 99, 2, 99])); // 100
console.log(biggestNumberInArray(['a',3,4,2])); // 4
console.log(biggestNumberInArray([])); // 0

// ================= Exercise 5: Unique Elements =================
function uniqueElements(arr) {
    return [...new Set(arr)];
}

console.log("Exercise 5:");
console.log(uniqueElements([1,2,3,3,3,3,4,5])); // [1,2,3,4,5]

// ================= Exercise 6: Calendar =================
function createCalendar(year, month) {
    const daysOfWeek = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"];
    const table = document.createElement("table");
    table.style.borderCollapse = "collapse";
    
    const thead = table.createTHead();
    const headRow = thead.insertRow();
    daysOfWeek.forEach(day => {
        const th = document.createElement("th");
        th.textContent = day;
        th.style.border = "1px solid black";
        th.style.padding = "3px 5px";
        headRow.appendChild(th);
    });

    const tbody = table.createTBody();
    const firstDay = new Date(year, month - 1, 1).getDay();
    const lastDay = new Date(year, month, 0).getDate();

    let date = 1;
    let weekDayIndex = (firstDay + 6) % 7;

    while (date <= lastDay) {
        const row = tbody.insertRow();
        for (let i = 0; i < 7; i++) {
            const cell = row.insertCell();
            cell.style.border = "1px solid black";
            cell.style.padding = "3px 5px";
            if ((date === 1 && i < weekDayIndex) || date > lastDay) {
                cell.textContent = "";
            } else {
                cell.textContent = date;
                date++;
            }
        }
    }

    document.body.appendChild(table);
}

createCalendar(2024, 8);