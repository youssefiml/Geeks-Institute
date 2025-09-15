#Exercise 1: What is the Season?

month = int(input("enter a month between 1 and 12 : "))

if month in [3, 4, 5]:
    season = "Spring"
elif month in [6, 7, 8]:
    season = "Summer"
elif month in [9, 10, 11]:
    season = "Autumn"
elif month in [12, 1, 2]:
    season = "Winter"
else:
    season = "Invalid month"

print(f"your season is : {season}")

#Exercise 2: For Loop test

for i in range(1, 21):
    print(i)

for index, value in enumerate(range(1, 21)):
    if index %2==0: print(value)
    
    
#Exercise 3: While Loop

my_name = "youssef"

while True:
    name = input("Enter your name : ")
    if my_name == name:
        print(f"We have same name {my_name}")
    break


#Exercise 4: Check the index

names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

user_name = input("Enter your name : ")

if user_name in names:
    print("index : ", names.index(user_name))
else:
    print("invalid name ")

#Exercise 5: Greatest Number

first_num = int(input(""))
seconde_num = int(input(""))
third_num = int(input(""))

greatest = max(first_num, seconde_num, third_num)

print(f"The greatest number is: {greatest}")

# Exercise 6: Random number
import random

wins = 0
losses = 0

while True:
    user_input = input("Guess a number from 1 to 9 (or type 'q' to quit): ")

    if user_input.lower() == 'q':
        break

    if not user_input.isdigit() or not (1 <= int(user_input) <= 9):
        print("Please enter a valid number from 1 to 9.")
        continue

    user_number = int(user_input)
    random_number = random.randint(1, 9)
    print(f"Random number is: {random_number}")

    if user_number == random_number:
        print("Winner!")
        wins += 1
    else:
        print("Better luck next time.")
        losses += 1

print("\nGame Over!")
print(f"Total games won: {wins}")
print(f"Total games lost: {losses}")