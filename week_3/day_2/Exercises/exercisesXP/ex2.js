const stock = { 
    "banana": 6, 
    "apple": 0,
    "pear": 12,
    "orange": 32,
    "blueberry": 1
}  

const prices = {    
    "banana": 4, 
    "apple": 2, 
    "pear": 1,
    "orange": 1.5,
    "blueberry": 10
} 

const shoppingList = ["banana", "orange", "apple"];

function myBill() {
    let totalPrice = 0;
    
    console.log("Processing your shopping list:");
    console.log("Items to purchase:", shoppingList);
    
    for (let item of shoppingList) {
        if (item in stock) {
            if (stock[item] > 0) {
                totalPrice += prices[item];
                console.log(`✅ ${item}: $${prices[item]} (stock: ${stock[item]})`);
                
                stock[item] -= 1;
                console.log(`   Stock updated: ${item} now has ${stock[item]} left`);
            } else {
                console.log(`❌ ${item}: Out of stock!`);
            }
        } else {
            console.log(`❌ ${item}: Item not found in inventory`);
        }
    }
    
    console.log(`Total bill: $${totalPrice}`);
    
    return totalPrice;
}

console.log("Initial stock:", stock);

const bill = myBill();

console.log("Updated stock after purchase:", stock)