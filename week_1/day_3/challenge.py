class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}
        
    def add_animal(self, animal_type, count=1):
        if animal_type in self.animals:
            self.animals[animal_type] += count
        else:
            self.animals[animal_type] = count
            
    def get_info(self):
        return self.animals
    
    def get_animal_types(self):
        return sorted(self.animals.keys())
    
    def get_short_info(self):
        animal_types = self.get_animal_types()
        animal_list = []

        for animal in animal_types:
            count = self.animals[animal]
            if animal == "sheep":
                animal_list.append("sheep")
            elif count > 1:
                animal_list.append(animal + "s")
            else:
                animal_list.append(animal)
                
        if len(animal_list) > 1:
            animals_str = ", ".join(animal_list[:-1]) + " and " + animal_list[-1]
        else:
            animals_str = animal_list[0]

        return f"{self.name} farm has {animals_str}."

macdonald = Farm("Macdonalds")
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)

print(macdonald.get_short_info())
