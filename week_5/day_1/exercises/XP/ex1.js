function compareToTen(num){
    let promise = new Promise((resolve, reject) => {
        if(num > 10){
            resolve(`${num} is greater than 10`)
        } else {
            reject(`${num} is less than 10`)
        }
    })
    return promise
}

compareToTen(15)
  .then(result => console.log(result))
  .catch(error => console.log(error))

compareToTen(8)
  .then(result => console.log(result))
  .catch(error => console.log(error))