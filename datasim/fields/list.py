import random

from .base import Field


class List(Field):
    def __init__(self, field:Field, min_length:int=1, max_length:int=5, func=None):
        super().__init__(func)

        if not isinstance(min_length, int) or not isinstance(max_length, int):
            raise TypeError("min_length and max_length must be integers")
        if min_length < 0 or max_length < 0:
            raise ValueError("min_length and max_length must be >= 0")
        if min_length > max_length:
            raise ValueError("min_length must be <= max_length")

        self.field = field
        self.min_length = min_length
        self.max_length = max_length

    def base_generation(self, context=None):
        length = random.randint(self.min_length, self.max_length)
        return [self.field.generate(context) for _ in range(length)]