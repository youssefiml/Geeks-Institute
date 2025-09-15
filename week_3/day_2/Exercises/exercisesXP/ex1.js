// function displayNumbersDivisible(){
//     let devisedNumbers = 0
//     let sum = 0
//     for (let i = 0; i <= 500 ;i++){
//         if (i % 23 === 0){
//             devisedNumbers += i + ' '
//             sum += i
//         }
//     }
//     console.log(devisedNumbers)
//     console.log(sum)
// }
// displayNumbersDivisible()

function displayNumbersDivisibleA(devisor){
    let devisedNumbers = 0
    let sum = 0
    for (let i = 0; i <= 500 ;i++){
        if (i % devisor === 0){
            devisedNumbers += i + ' '
            sum += i
        }
    }
    console.log(devisedNumbers)
    console.log(sum)
}
displayNumbersDivisibleA(3)
displayNumbersDivisibleA(45)