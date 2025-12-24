from .base import Field


class Str(Field):
    def __init__(self, func=None, length:int=10):
        super().__init__(func)
        
        self.length = length
    
    def base_generation(self, context=None) -> str:
        return "x" * self.length