#Exercise 1 : Pets

class Pets():
    def __init__(self, animals,):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
class siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
bengal_cat = bengal("Luffy", 3)
chartreux_cat = chartreux("Nami", 1)
siamese_cat = siamese("Leo", 2)

all_cats = [bengal_cat, chartreux_cat, siamese_cat]

sara_pets = Pets(all_cats)

sara_pets.walk()