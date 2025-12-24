import random

from .base import Field


class Nullable(Field):
    def __init__(self, field:Field, probability:float=0.5):
        super().__init__(func=None)

        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")

        self.field = field
        self.probability = probability

    def base_generation(self, context=None):
        if random.random() < self.probability:
            return None
        return self.field.generate(context)