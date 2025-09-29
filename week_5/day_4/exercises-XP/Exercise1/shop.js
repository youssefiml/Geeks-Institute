const products = require('./products');

function displayProducts() {
    console.log("Available Products:");
    products.forEach(product => {   
    console.log(`- ${product.name} ($${product.price}) - Category: ${product.category}`);
    });
};

console.log("Welcome to the Shop!");
displayProducts();