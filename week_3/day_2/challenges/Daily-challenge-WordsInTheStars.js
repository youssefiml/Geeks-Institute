// 1. Ask the user to enter words separated by commas
const input = prompt("Enter words separated by commas (e.g., Hello,World,in,a,frame)");

// 2. Convert the input string into an array of words
const words = input.split(",").map(word => word.trim());

// 3. Find the length of the longest word
const maxLength = Math.max(...words.map(word => word.length));

// 4. Create the top and bottom border made of asterisks
const border = "*".repeat(maxLength + 4); // +4 for two asterisks and spaces on both sides

console.log(border);

// 5. Print each word on a line with padding and stars
words.forEach(word => {
    const padding = " ".repeat(maxLength - word.length); // add spaces to align words
    console.log(`* ${word}${padding} *`);
});

console.log(border);