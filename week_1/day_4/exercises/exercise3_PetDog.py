#Exercise 3 : Dogs Domesticated

from week_1.day_4.exercises.exercise2_Dogs import Dog
import random

class PetDog(Dog):
    def __init__(self,name, age, height, trained = False):
        super().__init__(name, age, height)
        self.trained = trained
        
    def train(self):
        print(self.bark())
        self.trained = True
        
    def play(self, *args):
        dog_names = ', '.join([dog.name for dog in args])
        return f"{dog_names} all play together"
        # dog_names = [self.name] + [dog.name for dog in args]
        # if len(dog_names) > 1:
        #     names_str = ", ".join(dog_names[:-1]) + " and " + dog_names[-1]
        # else:
        #     names_str = dog_names[0]
        # return f"{names_str} all play together"
    
    def do_a_trick(self):
        if self.trained is True:
            sentences = [
            f"{self.name} does a barrel roll",
            f"{self.name} stands on his back legs",
            f"{self.name} shakes your hand",
            f"{self.name} plays dead"
            ]
            print(random.choice(sentences))

dog1 = PetDog("Max", 2, 20, True)
dog2 = PetDog("Mari", 1, 12, True)
dog3 = PetDog("Robin", 5, 17, )

print(dog1.play(dog1, dog2, dog3))