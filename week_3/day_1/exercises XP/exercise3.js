let num = prompt("Please enter a number:");
let type = typeof num;
while (typeof num === "string" && Number(num) < 10) {
    num = prompt("Number is less than 10. Please enter a new number:");
}