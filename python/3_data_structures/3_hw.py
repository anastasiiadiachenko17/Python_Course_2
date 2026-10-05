"""Basic operations on Python's four built-in collection types.

Demonstrates list, tuple, set and dict using only their core capabilities:
no comprehensions, lambdas or functions, as the exercise requires.
"""

fruits = ['apple', 'banana', 'cherry', 'potato']  # Mutable and ordered.
colors = ('red', 'white', 'green')  # Immutable: no add or remove.
numbers = {1, 2, 3}  # Unordered, stores unique values only.
person = {"Taras": 25}  # Maps a name to an age.

fruits.append("grape")
print(fruits)

# remove() deletes the first match and raises ValueError if the value is absent.
fruits.remove("potato")
print(fruits)

# The "in" operator evaluates to a bool, so no if statement is needed here.
print("apple" in fruits)

print(len(colors))

# add() silently does nothing if the value is already in the set.
numbers.add(4)
print(numbers)

# Assigning to a key that does not exist yet inserts a new pair.
person["Sasha"] = 26
print(person)
