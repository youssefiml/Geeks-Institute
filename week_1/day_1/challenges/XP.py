#Challenge 1

number = int(input("enter a number : "))
length = int(input("enter a lenght : "))

multiples = [number * i for i in range(1, length + 1)]

print(multiples)

#Challenge 2

word = input("Enter a word: ")

if word:
    new_word = word[0]
else:
    new_word = ""

for char in word[1:]:
    if char != new_word[-1]:
        new_word += char

print("New word without consecutive duplicates:", new_word)
