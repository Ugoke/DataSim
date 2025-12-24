

class Field:
    def __init__(self, func=None):
        if func is not None and not callable(func):
            raise TypeError("func must be a callable or None")
        self.func = func

    def generate(self, context=None):
        if self.func:
            if context:
                return self.func(context)
            return self.func()
        return self.base_generation(context)
    
    def base_generation(self, context=None):
        raise NotImplementedError("base_generation must be implemented")