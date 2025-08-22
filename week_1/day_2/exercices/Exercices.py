#Exercise 1 : Convert lists into dictionaries

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

my_dict = dict(zip(keys, values))

print(my_dict)


#Exercise 2 : Cinemax #2

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}


Tprice = 0

for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age < 12:
        price = 10
    else:
        price = 15
    print(f"{name} will pay : {price}")
    Tprice += price 
print(f"the family total cost for the movie : {Tprice}")


# Exercise 3: Zara

brand = {
    "name": "Zara", 
    "creation_date": 1975, 
    "creator_name": "Amancio Ortega Gaona", 
    "type_of_clothes": ["men, women, children, home"], 
    "international_competitors": ["Gap, H&M, Benetton"], 
    "number_stores": 7000, 
    "major_color": {
        "France": "blue", 
        "Spain": "red", 
        "US": "pink, green"
    }
}

brand.update({"number_stores": 2})

type_of_clothes = print(f"Zara is : /n{brand}")

brand["country_creation"] = "Spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")
    
brand.pop("creation_date")

print(brand["international_competitors"][-1])

print(brand["major_color"]["US"])

print(len(brand))

print(brand.keys())

more_on_zara = {
    "creation_date": 1975,
    "number_stores": 10000
}

brand.update(more_on_zara)
print(brand)

print(brand["number_stores"])

#Exercise 4 : Some Geography

def describe_city(city, country = "Maroc"):
    print(f"{city} is in {country}")
describe_city("Rabat")

#Exercise 5 : Random

import random

def guess_number(user_number):
    if not 1 <= user_number <= 100:
        print("Please enter a number between 1 and 100.")
        return
    
    random_number = random.randint(1, 100)
    
    if user_number == random_number:
        print(f"Great both numbers are {user_number}.")
    else:
        print(f"Your number was {user_number}, and the random number was {random_number}.")

    
# Exercise 6 : Let’s create some personalized shirts !

def make_shirt(size="Large", text="I love Python"):
    print(f"The size of the shirt is {size} and the text is '{text}'.")

make_shirt()

make_shirt("Medium")

make_shirt("Small", "Keep Calm and Code On")

make_shirt(size="XL", text="Hello World")
make_shirt(text="Debugging mode", size="Small")


#Exercise 7 : Temperature Advice

import random

def get_random_temp(season):
    if season == "winter":
        return round(random.uniform(-10, 16), 1)
    elif season == "spring":
        return round(random.uniform(5, 23), 1)
    elif season == "summer":
        return round(random.uniform(16, 40), 1)
    elif season == "autumn" or season == "fall":
        return round(random.uniform(0, 20), 1)
    else:
        return round(random.uniform(-10, 40), 1)
    
def main():
    month = int(input("Enter the month number (1 = Jan, 12 = Dec): "))

    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    elif month in [9, 10, 11]:
        season = "autumn"
    else:
        season = "unknown"

    temp = get_random_temp(season)

    print(f"\nThe temperature right now is {temp}°C in {season}.")

    if temp < 0:
        print("Brrr, that's freezing! Wear some extra layers today.")
    elif 0 <= temp < 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 <= temp < 23:
        print("Nice weather, enjoy your day!")
    elif 23 <= temp < 32:
        print("It's warm, perfect for a t-shirt!")
    elif 32 <= temp <= 40:
        print("It's really hot! Stay hydrated and cool.")
    else:
        print("Strange weather today... stay safe!")

main()

#Exercise 8 : Star Wars Quiz


data = [
    {"question": "What is Baby Yoda's real name?", "answer": "Grogu"},
    {"question": "Where did Obi-Wan take Luke after his birth?", "answer": "Tatooine"},
    {"question": "What year did the first Star Wars movie come out?", "answer": "1977"},
    {"question": "Who built C-3PO?", "answer": "Anakin Skywalker"},
    {"question": "Anakin Skywalker grew up to be who?", "answer": "Darth Vader"},
    {"question": "What species is Chewbacca?", "answer": "Wookiee"}
]

def play_quiz():
    correct = 0
    incorrect = 0
    wrong_answers = []

    for item in data:
        user_answer = input(item["question"] + " ").strip()

        if user_answer.lower() == item["answer"].lower():
            print("✅ Correct!")
            correct += 1
        else:
            print(f"❌ Wrong! The correct answer is {item['answer']}.")
            incorrect += 1
            wrong_answers.append({
                "question": item["question"],
                "your_answer": user_answer,
                "correct_answer": item["answer"]
            })

    return correct, incorrect, wrong_answers

def show_results(correct, incorrect, wrong_answers):
    print("\n--- Quiz Results ---")
    print(f"Correct answers: {correct}")
    print(f"Incorrect answers: {incorrect}")

    if wrong_answers:
        print("\nYou got these wrong:")
        for item in wrong_answers:
            print(f"Q: {item['question']}")
            print(f"   Your answer: {item['your_answer']}")
            print(f"   Correct answer: {item['correct_answer']}\n")

def main():
    while True:
        correct, incorrect, wrong_answers = play_quiz()
        show_results(correct, incorrect, wrong_answers)

        if incorrect > 3:
            print("You had more than 3 wrong answers. Let's try again!\n")
        else:
            print("Well done! Thanks for playing 🎉")
            break

main()