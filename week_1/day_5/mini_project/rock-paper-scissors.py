from game import Game

def get_user_menu_choice():
    choice = input("""
        Menu:
        (g) Play a new game
        (x) Show scores and exit
        :
    """)
    if choice == "g" or "x":
        return choice
    else:
        return "invalid"

def print_results(results):
    print("Game Result:")
    print(f"You won {results.get('win', 0)}")
    print(f"You lost {results.get('loss', 0)}")
    print(f"You drew {results.get('draw', 0)}")
    print("Thank you for playing!")
    
def main():
    results = {"win" : 0, "loss" : 0, "draw" : 0}
    while True:
        choice = get_user_menu_choice()
        if choice == "invalid":
            print("Please choose just 'g' or 'x'")
            continue
        if choice == "g":
            my_game = Game(["rock", "paper", "scissors"])
            result = my_game.play()
            results[result] += 1
        elif choice == "x":
            print_results(results)
            break
        
if __name__ == "__main__":
    main()