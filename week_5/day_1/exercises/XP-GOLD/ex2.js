function timesTwoAsync(x) {
  return new Promise(resolve => resolve(x * 2));
}

const arr = [1, 2, 3];
const promiseArr = arr.map(timesTwoAsync);
// promiseArr = [
//   Promise.resolve(2),   // 1 * 2
//   Promise.resolve(4),   // 2 * 2
//   Promise.resolve(6)    // 3 * 2
// ]


Promise.all(promiseArr)
  .then(result => {
    console.log(result);
  });

// ✅ [2, 4, 6]