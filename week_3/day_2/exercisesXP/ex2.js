const stock = { 
    "banana": 6, 
    "apple": 0,
    "pear": 12,
    "orange": 32,
    "blueberry":1
};

const prices = {    
    "banana": 4, 
    "apple": 2, 
    "pear": 1,
    "orange": 1.5,
    "blueberry":10
};

let shoppingList =  stock["banana", "apple", "orange"];

function myBill(){
    if (stock["banana"] > 0){
        let bananaPrice = 4
    } else if (stock["apple"] > 0){
        let applePrice = 2
    } else if (stock["orange"] > 0){
        let orangePrice = 1.5
    }
    let totalPrices = bananaPrice + applePrice + orangePrice
    return totalPrices
}

console.log(myBill())