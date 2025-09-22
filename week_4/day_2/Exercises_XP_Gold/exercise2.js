const result = [[0, 1], [2, 3]].reduce(
  (acc, cur) => {
    return acc.concat(cur);
  },
  [1, 2]
);

console.log(result);

// 1st iteration:
// acc = [1, 2]
// cur = [0, 1]
// acc.concat(cur) → [1, 2, 0, 1]

// 2nd iteration:
// acc = [1, 2, 0, 1] (result of previous step)
// cur = [2, 3]
// acc.concat(cur) → [1, 2, 0, 1, 2, 3]

// Final result returned by reduce → [1, 2, 0, 1, 2, 3]
