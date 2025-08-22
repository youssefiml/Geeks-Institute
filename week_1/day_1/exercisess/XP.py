#Exercice 1

print("hello world\nhello world\nhello world\nhello world")


#Exercice 2

num1 = 99 * 99 * 99
num2 = 8
rslt = num1 * num2
print (f"the result is : {rslt}")

#exercice 3 

my_name = "youssef"
user_name = input("what is your name : \n" )

if my_name == user_name.lower().strip():
    print("LOL we have the same name ")
else:
    print("nice to meet you " + user_name)


#exercice 4

user_height = int(input("Enter your height in cm : "))

if user_height >= 145:
    print("Welcome, you are tall enough to ride ")
else:
    print("Sorry, you are not tall enough to ride ")

#exercice 5

my_fav_numbers = {5, 9, 10}
print("my favorite numbers : ", my_fav_numbers)

my_fav_numbers.add(7)
my_fav_numbers.add(6)

my_fav_numbers.pop()

friend_fav_numbers = {9, 3, 5, 7}
print("my friend favorite numbers : ", my_fav_numbers)

our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print("our favorite numbers : ", our_fav_numbers)

#exercice 7

basket = ["Banana", "Apples", "Oranges", "Blueberries"]

basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")

apple_count = basket.count("Apples")
print("Number of Apples:", apple_count)

basket.clear()

print(basket)

#exercice 8

sandwich_order = [
    "Tuna sandwich", 
    "Pastrami sandwich", 
    "Avocado sandwich", 
    "Pastrami sandwich", 
    "Egg sandwich", 
    "Chicken sandwich", 
    "Pastrami sandwich"
]

print("Sorry, the deli has run out of pastrami!")

while "Pastrami sandwich" in sandwich_order:
    sandwich_order.remove("Pastrami sandwich")

finished_sandwiches = []

while sandwich_order:
    current_sandwich = sandwich_order.pop(0)
    print(f"I made your {current_sandwich}")
    finished_sandwiches.append(current_sandwich)
