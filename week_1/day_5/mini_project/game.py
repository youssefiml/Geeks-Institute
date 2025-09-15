import random

class Game:
    def __init__(self, items):
        self.items = ["rock", "paper", "scissors"]
        
    def get_user_item(self):
        while True:
            user_item = input("select rock, paper or scissor :").lower()
            if user_item in self.items:
                return user_item
            else:
                print("Invalid item :(")
    
    def get_computer_item(self):
        computer_item = random.choice(self.items)
        return computer_item
    
    def get_game_result(self, user_item, computer_item):
        if user_item == computer_item:
            return "draw"
        elif (
            (user_item == "rock" and computer_item == "scissors") or 
            (user_item == "paper" and computer_item == "rock") or 
            (user_item == "scissors" and computer_item == "paper")
        ):
            return "win"
        else:
            return "loss"
        
    def play(self):
        user_choice = self.get_user_item()
        computer_choise = self.get_computer_item()
        result = self.get_game_result(user_choice, computer_choise)
        if result == "draw":
            print(f"You choose: '{user_choice}'\n The computer choose: '{computer_choise}'\n Result: Draw")
        elif result == "win":
            print(f"You choose: '{user_choice}'\n The computer choose: '{computer_choise}'\n Result: Win")
        else:
            print(f"You choose: '{user_choice}'\n The computer choose: '{computer_choise}'\n Result: loss")
        return result
    
    