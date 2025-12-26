# 🧩 Create your own Writer types
## Basic rules
- A custom `Writer` type must inherit from `Writer`
- The generation logic is implemented in the `write(self, path, rows)` method

## The simplest example: a custom `CSVWriter`
```python
import csv
from datasim import Writer

class CSVWriter(Writer):
    def write(self, path, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
```
### What's going on here:
- `CSVWriter` inherits from `Writer`
- The `write()` method is implemented to write the rows of data to a CSV file using Python's `csv.DictWriter`
- `path` is the file where the data will be saved, and `rows` is the list of dictionaries to write
---
## Using a custom `Writer`
```python
from datasim import BaseDataGen, Sequence, Str

class UserData(BaseDataGen):
    __count__ = 10
    __file_type__ = CSVWriter  # Specify the custom writer here

    id: Sequence()
    name: Str()

UserData.generate("data.csv")
```