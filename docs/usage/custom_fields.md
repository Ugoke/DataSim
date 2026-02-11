# 🧩 Create your own field types
## Basic rules
- A custom type must inherit from `Field`
- The generation logic is implemented in the `base_generation(self, context=None)` method
- The `base_generation` method must return the generated value
- `func` support is already implemented in `Field` - it usually doesn't need to be reimplemented
---
## The simplest example: a custom type `Bool`
```python
import random
from datasim import BaseDataGen, Str, Int, Field

class Bool(Field):
    def __init__(self, func=None):
        super().__init__(func)

    def base_generation(self, context=None):
        return bool(random.getrandbits(1))
```
### What's going on here
- `Bool` inherits from `Field`
- All custom logic is implemented in `base_generation`
- The field automatically supports `func` if one is passed
---
## Using a custom field
```python
class User(BaseDataGen):
    __count__ = 10

    id = Int(min=1, max=100)
    username = Str()
    is_staff = Bool()

User.generate_and_save("data.csv", "csv")
```
## Using `context` in custom fields
### The `base_generation` method takes a `context` argument - a dictionary with already generated fields of the current row.
```python
class IsAdult(Field):
    def base_generation(self, context=None):
        return context["age"] >= 18
```
```python
class User(BaseDataGen):
    age = Int(min=1, max=90)
    is_adult = IsAdult()
```

⚠️ Important
The fields are generated sequentially in the order they are declared.
A custom field can only access the fields declared above.