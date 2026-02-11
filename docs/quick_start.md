# 🚀 Quick Start

### 🛠️ 1. Creating a Data Schema
Create a Python file in which you define a class with fields for generating data. Example:

```python
from datasim import BaseDataGen, Int, Str

class UserData(BaseDataGen):
    __count__ = 100  # Number of rows to generate
    id = Int(min=1, max=1000)  # Generating integers
    name = Str()  # Generating Strings

data = UserData.generate() #At this point no data is generated yet. Data generation happens automatically on first access.

data.save("users.csv", "csv")
```

### 🚀 2. Start generation
#### Run the script to generate data and save it to the `user_data.csv` file.

## That's it!