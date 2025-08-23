#Exercise 1: Cats

class cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age
    
cat1 = cat("Nami", 2)
cat2 = cat("Robin", 1)
cat3 = cat("Oscar", 4)
    
def find_oldest(cats):
        return max(cats, key=lambda c: c.age)
    
oldest = find_oldest([cat1, cat2, cat3])
    
print(f"The oldest cat is {oldest.name}, and is {oldest.age} years old.")


#Exercise 2 : Dogs

class dog:
    def __init__(self, dog_name, dog_height):
        self.name = dog_name
        self.height = dog_height
        
    def bark(self):
        print(f"{self.name} goes woof!")
        
    def jump(self):
        x = self.height * 2
        print(f"{self.name} jumps {x} cm high!")
        
davids_dog = dog("Rex", 50)

print(davids_dog.bark(), davids_dog.jump())

sarahs_dog = dog("Teacup", 20)

print(sarahs_dog.bark(), sarahs_dog.jump())

if sarahs_dog.height < davids_dog.height:
    print(f"the bigger is : {davids_dog.name}")
else:
    print(f"the bigger is : {sarahs_dog.name}")
    
#Exercise 3 : Who’s the song producer?

class song:
    def __init__(self, lyrics):
        self.lyrics = lyrics
        
    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)
        
stairway = song(["There's a lady who's sure","all that glitters is gold", "and she's buying a stairway to heaven"])
stairway.sing_me_a_song()


#Exercise 4 : Afternoon at the Zoo

class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []

    def add_animal(self, new_animal):
        if new_animal not in self.animals:
            self.animals.append(new_animal)

    def get_animals(self):
        for animal in self.animals:
            print(animal)

    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)

    def sort_animals(self):
        sorted_animals = sorted(self.animals)
        self.groups = {}
        for animal in sorted_animals:
            first_letter = animal[0].upper()
            if first_letter not in self.groups:
                self.groups[first_letter] = []
            self.groups[first_letter].append(animal)

    def get_groups(self):
        for key, value in self.groups.items():
            print(f"{key}: {', '.join(value)}")


new_york_zoo = Zoo("New York Zoo")
new_york_zoo.add_animal("Lion")
new_york_zoo.add_animal("Leopard")
new_york_zoo.add_animal("Elephant")
new_york_zoo.add_animal("Eagle")
new_york_zoo.add_animal("Zebra")

new_york_zoo.get_animals()

new_york_zoo.sell_animal("Leopard")
print("After selling Leopard:")
new_york_zoo.get_animals()

new_york_zoo.sort_animals()
new_york_zoo.get_groups()
