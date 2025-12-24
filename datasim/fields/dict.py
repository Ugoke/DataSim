from .base import Field


class Dict(Field):
    def __init__(self, schema, func=None):
        super().__init__(func)

        if not isinstance(schema, dict) or not all(isinstance(v, Field) for v in schema.values()):
            raise TypeError("schema must be a dict of str -> Field")
        self.schema = schema

    def base_generation(self, context=None):
        result = {}
        for key, field in self.schema.items():
            result[key] = field.generate({**context} if context else None)
        return result