import sys

#Exercise 1 : Outputs
# True
# True
# False
# False
# True
# False

#x is True
#y is False
a = 4
b = 10


#Exercise 2 : Longest word without a specific character

sentence = input("Enter a longest sentence without the character “A” : ")


#

import re

from collections import Counter

paragraph = """
The sun dipped below the horizon, casting a golden hue over the tranquil sea. 
Waves gently lapped against the shore, whispering tales of distant lands.
"""

words = re.findall(r'\b\w+\b', paragraph.lower())

total_chars = len(paragraph)

non_whitespace_chars = len(paragraph.replace(" ", ""))

sentences = re.split(r'[.!?]', paragraph.strip())
sentences = [s for s in sentences if s]
total_words = len(words)
unique_words = len(set(words))
avg_words_per_sentence = total_words / len(sentences) if sentences else 0
non_unique_words = total_words - unique_words

print(f"Total characters (including spaces): {total_chars}")
print(f"Total sentences: {len(sentences)}")
print(f"Total words: {total_words}")
print(f"Unique words: {unique_words}")
print(f"Non-whitespace characters: {non_whitespace_chars}")
print(f"Average words per sentence: {avg_words_per_sentence:.2f}")
print(f"Non-unique words: {non_unique_words}")
