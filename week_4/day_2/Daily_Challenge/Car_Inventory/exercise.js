const inventory = [
  { id: 1, car_marke: "Lincoln", car_model: "Navigator", car_year: 2009 },
  { id: 2, car_marke: "Mazda", car_model: "Miata MX-5", car_year: 2001 },
  { id: 3, car_marke: "Honda", car_model: "Accord", car_year: 1983 },
  { id: 4, car_marke: "Land Rover", car_model: "Defender Ice Edition", car_year: 2010 },
  { id: 5, car_marke: "Honda", car_model: "Accord", car_year: 1995 },
];

//Part 1
function getCarHonda(carInventory) {
  const hondaCar = carInventory.find(car => car.car_marke === "Honda");
  return `This is a ${hondaCar.car_marke} ${hondaCar.car_model} from ${hondaCar.car_year}.`;
}
//Part 2
function sortCarInventoryByYear(carInventory) {
  return carInventory.sort((a, b) => a.car_year - b.car_year);
}

console.log(getCarHonda(inventory));

console.log(sortCarInventoryByYear(inventory));
