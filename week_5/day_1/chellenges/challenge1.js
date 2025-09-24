function makeAllCaps(words){
    return new Promise((resolve, reject) => {
        if(words.every(word => typeof word === 'string')){
            const caps = words.map(word => word.toUpperCase());
            resolve(caps);
        } else {
            reject('Not a string!');
        }
    });
}

function sortWords(words){
    return new Promise((resolve, reject) => {
        if(words.length > 4){
            resolve(words.sort());
        } else {
            reject('Array length is less than 4');
        }
    });     
}

makeAllCaps([1, "pear", "banana"])
      .then((arr) => sortWords(arr))
      .then((result) => console.log(result))
      .catch(error => console.log(error))

makeAllCaps(["apple", "pear", "banana"])
      .then((arr) => sortWords(arr))
      .then((result) => console.log(result))
      .catch(error => console.log(error))

makeAllCaps(["apple", "pear", "banana", "melon", "kiwi"])
      .then((arr) => sortWords(arr))
      .then((result) => console.log(result))
      .catch(error => console.log(error))