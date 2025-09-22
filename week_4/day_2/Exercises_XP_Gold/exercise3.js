const arrayNum = [1, 2, 4, 5, 8, 9];

const newArray = arrayNum.map((num, i) => {
  // `num` → current element
  // `i`   → index of the current element

  console.log("Current Number:", num, "| Index (i):", i); 
  // Displays both the number and its index in the terminal

  // alert(num); //  Remove this, works only in browser
  console.log("Alert Simulation:", num); //  Simulated alert for Node.js

  return num * 2; // Double each number
});

console.log("Resulting newArray:", newArray);

/*
Answer to the Question:
The value of `i` is the index of the current element in the array,
starting from 0 and incrementing by 1 for each iteration.

For the array [1, 2, 4, 5, 8, 9], `i` will take the values:
0, 1, 2, 3, 4, 5
*/
