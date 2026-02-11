import random
from tqdm import tqdm

from datasim.generators.row import RowGenerator
from datasim.writers import get_writer


class DatasetGenerator:
    def __init__(self, schema):
        self._schema = schema
        self._fields = schema._fields
        self._count = schema.__count__
        self._log = schema.__log__
        self._rows = None
        
        if schema.__seed__ is not None:
            random.seed(schema.__seed__)


    def _generate_rows(self):
        if self._rows is not None:
            return self._rows

        rows = []
        row_gen = RowGenerator(self._fields)
        iterator = tqdm(range(self._count)) if self._log else range(self._count)

        for _ in iterator:
            rows.append(row_gen.generate())

        self._rows = rows
        return rows


    def save(self, path, file_type):
        writer = get_writer(file_type)
        rows = self._generate_rows()
        writer.write(path, rows)


    def head(self, n=5):
        rows = self._generate_rows()
        return rows[:n]
    

    def tail(self, n=5):
        rows = self._generate_rows()
        return rows[-n:]
    

    def all(self):
        return self._generate_rows()
    

    def len(self):
        return len(self._generate_rows())