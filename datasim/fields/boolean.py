import random

from .base import Field


class Bool(Field):
    def __init__(self, func=None):
        super().__init__(func)

    def base_generation(self, context=None):
        return bool(random.getrandbits(1))