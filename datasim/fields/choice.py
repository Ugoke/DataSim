import random

from .base import Field


class Choice(Field):
    def __init__(self, values, *, func=None):
        super().__init__(func)

        self.values = tuple(values)
        if not self.values:
            raise ValueError("Choice values cannot be empty")

    def base_generation(self, context=None):
        return random.choice(self.values)