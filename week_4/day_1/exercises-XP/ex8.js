function makeJuice(size){
    let ingredients = [];
    return { 
        addIngredients: function (ing1, ing2, ing3){
            ingredients.push(ing1, ing2, ing3);
        },
        displayJuice: function(){
            console.log(`The client wants a ${size} juice, containing ${ingredients.join(", ")}`);
        }
    }
}
let juice = makeJuice("Midium");
juice.addIngredients("apple", "banana", "orange");
juice.addIngredients("strawberry", "kiwi", "mango");
juice.addIngredients("peach", "pear", "grape");
juice.displayJuice();