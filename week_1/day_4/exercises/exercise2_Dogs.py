#Exercise 2 : Dogs

class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        
    def bark(self):
        return f"{self.name} is barking"
    
    def run_speed(self):
        return self.weight/self.age*10
    
    def fight(self, other_dog):
        power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if power > other_power:
            return f"the winner is {self.name}"
        else:
            return f"the winner is {other_dog.name}"

        
dog1 = Dog("Max", 3, 20)
dog2 = Dog("Leo", 2, 25)
dog3 = Dog("Ronaldo", 4, 15)

print(dog1.bark())
print(dog2.run_speed())
print(dog3.fight(dog3))