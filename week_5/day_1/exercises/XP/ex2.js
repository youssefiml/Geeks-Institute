new Promise((resolve) => {
    setTimeout(() => {
        resolve('success')
    }, 4000)
})

.then(result => console.log(result));