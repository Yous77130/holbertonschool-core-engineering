#!/usr/bin/env python3
"""Module demonstrating inheritance and polymorphism."""


class Animal:
    """A class that represents an animal."""

    def speak(self):
        """Return the sound of the animal."""
        return "Some sound"


class Dog(Animal):
    """A class that represents a dog."""

    def speak(self):
        """Return the sound of a dog."""
        return "Woof"


class Cat(Animal):
    """A class that represents a cat."""

    def speak(self):
        """Return the sound of a cat."""
        return "Meow"


animals = [Dog(), Cat(), Dog()]
for animal in animals:
    print(animal.speak())

dog = Dog()
print(isinstance(dog, Dog))
print(isinstance(dog, Animal))
print(issubclass(Dog, Animal))
