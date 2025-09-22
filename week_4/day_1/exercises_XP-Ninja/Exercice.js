const mergeWords = (string) => (nextString) => 
    nextString === undefined 
        ? string
        : mergeWords(string + ' ' + nextString);

// Example 1:
console.log(mergeWords('Hello')()); 

// Example 2:
console.log(
    mergeWords('There')('is')('no')('spoon.')()
); 

// Example 3:
console.log(
    mergeWords('JavaScript')('is')('fun')('and')('powerful.')()
); 