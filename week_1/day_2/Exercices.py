#Exercise 1 : Convert lists into dictionaries

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

my_dict = dict(zip(keys, values))

print(my_dict)


#Exercise 2 : Cinemax #2

name = input("Enter your name : ")
age = int(input("Enter your age : "))

my_dict1 = {}

for name, age in my_dict1:
    if age < 3:
        print("Ticket is free.")
    elif age >= 3 and age <12:
        print("The ticket is $10.")
    else:
        print("ticket is $15.")