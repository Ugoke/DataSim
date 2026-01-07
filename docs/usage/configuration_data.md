# ⚙️ Class Configuration

## 1. The main class `BaseDataGen`
### Each data class must inherit from `BaseDataGen`, which sets basic parameters such as the number of records and the type of file to which the data will be written.
```python
from datasim import BaseDataGen, Int

class UserData(BaseDataGen):
    __count__ = 100  # Number of records that will be generated
    __file_type__ = "csv"  # Output file format (CSV, JSON)
    __seed__ = None # Optional seed for reproducible data generation
    __log__ = True # Logging
    
    id: Int(min=1, max=1000)
```
- `__count__` - the number of records to be generated. If not specified, the value will be 100
- `__file_type__` - output file format (e.g. `"csv"` or `"json"`). If you don’t specify anything, it will default to csv
- `__seed__` - providing a seed ensures reproducible data generation across runs
- `__log__` - enables or disables logging of the data generation process

## 2. Defining fields
### All fields inherit from the base class `Field` and must be used as annotated attributes within a class that inherits from `BaseDataGen`.
---


### 2.1 Numeric fields: `Int`, `Float`, `Sequence`
### `Int`
```python
Int(min: int = 0, max: int = 100, func = None)
```
#### What does
- Returns a random integer between `min` and `max` inclusive (`random.randint`).
#### Example
```python
age: Int(min=18, max=90)
```
---
### `Float`
```python
Float(min: int|float = 0, max: int|float = 99.99, func = None, precision: int = 2)
```
#### What does
- Takes `random.uniform(min, max)` and rounds to `precision` decimal places (if `precision` is specified).
#### Example
```python
price: Float(min=0, max=999.99, precision=2)
```
---
### `Sequence`
```python
Sequence(start: int = 1, step: int = 1)
```
#### What does
- Returns sequential values: `start`, `start + step`, `start + 2*step`, ...
- Important: `Sequence` stores an internal `_current` state between data generation calls. This means that values are not automatically reset when `BaseDataGen.generate` is called again in the same process.
#### Example
```python
id: Sequence(start=1000, step=1)
```
---


### 2.2 String field: `Str`
```python
Str(func = None, length: int = 10)
```
#### What does
- By default, returns a string of `length` equal to the number of identical characters `"x"` (placeholder).
- For realistic values, it is recommended to pass `func` or replace the logic with your own implementation.
- Current behavior - placeholder. If you need random/human-like strings, use `func` (e.g., generator from `faker`).
#### Example
```python
username: Str(length=8)
```
---


### 2.3 Boolean type: `Bool`
```python
Bool(func = None)
```
#### What does
- Returns `True`/`False` randomly (`random.getrandbits(1)`).
#### Example
```python
is_active: Bool()
```
---


### 2.4 Select from a list: `Choice`
```python
Choice(values: Iterable, *, func = None)
```
#### What does
- Returns a random element from `values` ​​(`random.choice`).
#### Example
```python
status: Choice(["new", "processing", "done"])
```
---


### 2.5 `Nullable` - field that can return `None` with a probability
```python
Nullable(field: Field, probability: float = 0.5)
```
#### What does
- Returns `None` with probability `probability`, otherwise delegates to `field`.
#### Example
```python
middle_name: Nullable(Str(length=6), probability=0.7)
```
---


### 2.6 Date and time: `Date` and `DateTime`
### `Date`
```python
Date(start: date|str, end: date|str, *, func = None)
```
#### What does
- `start` and `end` can be `datetime.date` objects or ISO strings (`YYYY-MM-DD`).
- Returns a random date between `start` and `end` (by days)
#### Example
```python
joined_at: Date("2020-01-01", "2024-12-31")
```
---
### `DateTime`
```python
DateTime(start: datetime|str, end: datetime|str, *, tz: Optional[str] = None, func = None)
```
#### What does
- `start`/`end` - `datetime` or ISO string (`YYYY-MM-DDTHH:MM:SS`).
- Returns a random `datetime` between `start` and `end` (accurate to seconds).
- If `tz` is specified, `pytz.timezone(tz)` is used and the returned `datetime` is translated into this zone.
#### Example
```python
created_at: DateTime("2024-01-01T00:00:00", "2025-01-01T00:00:00", tz="Europe/Kyiv")
```
---


### 2.7 Lists and Dictionaries: `List` and `Dict`
### `List`
```python
List(field: Field, min_length: int = 1, max_length: int = 5, func = None)
```
#### What does
- Generates a list of length `random.randint(min_length, max_length)` elements.
- Each element is created by calling `field.generate(context)` (the same `context` is passed).
#### Example
```python
tags: List(Str(length=5), min_length=0, max_length=8)
```
---
### `Dict`
```python
Dict(schema: Dict[str, Field], func = None)
```
#### What does
- `schema` - dictionary `key -> Field`.
- Returns a dictionary where for each key the corresponding field is called.
#### Example
```python
address: Dict({
    "street": Str(length=12),
    "city": Str(length=8),
    "zip": Int(min=10000, max=99999)
})
```
---


### 2.8 User defined functions (`func`) - using `context`
#### Most fields support an optional `func` in the constructor. This is a powerful way to create fields with arbitrary logic or integrate external generators (e.g., `faker`).
#### Rules
- `func` must be callable. `Field.__init__` checks the type.
- `func` is called `func()` if there is no `context`, or `func(context)` if there is a context.

### ⚠️ Field generation order matters. Fields are generated sequentially in the order they are defined in the class. If a field uses `context`, it can only access fields defined above it.
```python
def custom_func(context: dict | None) -> Any:
    ...
```
#### Example
```python
from datasim import BaseDataGen, Int, Str

def returnNameAndNum(context=None) -> str:
    return "Name" + str(context["id"])

class User(BaseDataGen):
    __count__ = 3
    __seed__ = 42

    id: Int()
    name: Str(returnNameAndNum)

User.generate("data.csv")
```
#### What happens during generation
#### For each line:
1. Generated `id` (for example `1`)
2. In context appears:
```json
{"id": 1}
```
3. Called:
```python
returnNameAndNum(context)
```
4. Returns:
```text
"Name1"
```
5. Summary line:
```json
{"id": 1, "name": "Name1"}
```
---


### 2.9 Using `faker` for realistic data
#### Many fields support a custom `func`, which makes integration with `faker` straightforward and flexible.
##### Basic usage
```python
from faker import Faker
from datasim import BaseDataGen, Str, Int

fake = Faker()

class User(BaseDataGen):
    __count__ = 10
    __file_type__ = "json"

    id: Int(min=1, max=1000)
    username: Str(lambda _: fake.user_name())
    email: Str(lambda _: fake.email())

User.generate("data.json")
```
---
##### Reproducible faker data
To generate reproducible fake data, set the faker seed together with `__seed__`.
```python
from faker import Faker
from datasim import BaseDataGen, Str, Int

seed = 42

fake = Faker()
fake.seed_instance(seed)

class User(BaseDataGen):
    __count__ = 10
    __seed__ = seed

    id: Int(min=1, max=1000)
    username: Str(lambda _: fake.user_name())
    email: Str(lambda _: fake.email())

User.generate("data.csv")
```


## 3. Data generation
### Supported formats (from writers.get_writer):
- `"csv"` -> `CSVWriter` (creates a CSV file with a header from the keys in the first row)
- `"json"` -> `JSONWriter` (dump with `indent=4`, `ensure_ascii=False`)
- Otherwise - `ValueError("Unsupported file format: ...")`.
---


## 4. Useful templates and complex examples
### Simple example
```python
from datasim import BaseDataGen, Int, Str, DateTime, Bool

def returnNameAndNum(context=None) -> str:
    return "Name" + str(context["id"])

class UserData(BaseDataGen):
    __count__ = 50
    __file_type__ = "json"
    __seed__ = 42

    id: Int(min=1, max=1000)
    username: Str(returnNameAndNum)
    is_active: Bool()
    created_at: DateTime("2023-01-01T00:00:00", "2024-12-31T23:59:59", tz="UTC")

UserData.generate("data.json")
```
---
### Complex example with nested structures and context
```python
from datasim import BaseDataGen, Int, Choice, Nullable, List, Dict, Str, Sequence, Float

def returnNameAndStatus(context=None) -> str:
    return "Name" + context["status"]

class OrderData(BaseDataGen):
    __count__ = 100
    __seed__ = 42

    order_id: Sequence(start=1000, step=1)
    user_id: Int(min=1, max=500)
    status: Choice(["new", "paid", "shipped", "cancelled"])
    items: List(Dict({
        "product_id": Int(min=1, max=200),
        "qty": Int(min=1, max=5),
        "price": Float(min=1, max=500, precision=2)
    }), min_length=1, max_length=5)
    comment: Nullable(Str(returnNameAndStatus), probability=0.8)

OrderData.generate("data.csv")
```