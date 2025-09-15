function hotelCost(nights) {
    return nights * 140;
}

function planeRideCost(destination) {
    if (destination.toLowerCase() === "london") return 183;
    if (destination.toLowerCase() === "paris") return 220;
    return 300;
}

function rentalCarCost(days) {
    let cost = days * 40;
    if (days > 10) cost *= 0.95;
    return cost;
}

function totalVacationCost() {
    const nights = Number(prompt("How many nights?"));
    const destination = prompt("Destination?");
    const days = Number(prompt("Car rental days?"));

    const hotel = hotelCost(nights);
    const plane = planeRideCost(destination);
    const car = rentalCarCost(days);

    console.log(`The car cost: $${car}, the hotel cost: $${hotel}, the plane tickets cost: $${plane}.`);
    return hotel + plane + car;
}