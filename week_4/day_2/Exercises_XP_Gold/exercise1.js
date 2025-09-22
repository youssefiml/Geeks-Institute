const result = [1, 2, 3].map(num => {
  if (typeof num === 'number') {
    return num * 2;
  }
  return;
});

console.log(result); 

// Explanation:
// 1. map() iterates through each element of the array [1, 2, 3].
// 2. For each element (num):
//    - typeof num === 'number' → true for 1, 2, and 3
//    - So, it returns num * 2.
// 3. The return statement after the if would only run if num was NOT a number,
//    but in this case, it's never reached.
