function findAvg(gradesList){
    average = 0
    for (let i = 0; i < gradesList.length; i++){
        average += gradesList[i]
    }
    return average / gradesList.length
}

const avg = findAvg([55, 1000, 11, 76])
if (avg > 65){
    console.log("You passed")
} else {
    console.log('You failed and must repeat the course')
}

console.log(`the average is : ${average}`)