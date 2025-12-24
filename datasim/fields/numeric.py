import random

from .base import Field


class Int(Field):
    def __init__(self, min:int=0, max:int=100, func=None):
        super().__init__(func)

        if not isinstance(min, int) or not isinstance(max, int):
            raise TypeError("min and max must be integers")
        
        if min > max:
            raise ValueError("min must be <= max")
        
        self.min = min
        self.max = max

    def base_generation(self, context=None) -> int:
        return random.randint(self.min, self.max)
    

class Float(Field):
    def __init__(self, min:int|float=0, max:int|float=99.99, func=None, precision:int=2):
        super().__init__(func)
        try:
            self.min = float(min)
            self.max = float(max)
        except (TypeError, ValueError):
            raise TypeError("min and max must be numbers")
        
        if self.min > self.max:
            raise ValueError("min must be <= max")

        if not isinstance(precision, int) or precision < 0:
            raise ValueError("precision must be a non-negative int")

        self.precision = precision

    def base_generation(self, context=None) -> float:
        value = random.uniform(self.min, self.max)

        if self.precision is not None:
            value = round(value, self.precision)

        return value
    

class Sequence(Field):
    def __init__(self, start:int=1, step:int=1):
        super().__init__(func=None)

        if not isinstance(start, int) or not isinstance(step, int):
            raise TypeError("start and step must be integers")

        self._current = start
        self._step = step

    def base_generation(self, context=None) -> int:
        value = self._current
        self._current += self._step
        return value