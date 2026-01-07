import random
from tqdm import tqdm

from datasim.generators.row import RowGenerator
from datasim.writers import get_writer


class DatasetGenerator:
    def __init__(self, schema):
        self.schema = schema
        self.fields = schema._fields
        self.count = schema.__count__
        self.writer = get_writer(schema.__file_type__)
        self.log = schema.__log__
        
        if schema.__seed__ is not None:
            random.seed(schema.__seed__)


    def write(self, path):
        rows = []
        row_gen = RowGenerator(self.fields)

        iterator = tqdm(range(self.count)) if self.log else range(self.count)
        
        for _ in iterator:
            rows.append(row_gen.generate())

        self.writer.write(path, rows)