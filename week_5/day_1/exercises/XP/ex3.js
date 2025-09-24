Promise.resolve(3)
.then(value => console.log(value));

Promise.reject("Boo!")
.catch(error => console.log(error));