

class RowGenerator:
    def __init__(self, fields):
        self.fields = fields

    def generate(self):
        row = {}
        for name, field in self.fields.items():
            row[name] = field.generate(context=row)
        return row