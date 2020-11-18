# TypedCsv

Typed extension for default [csv library](https://docs.python.org/3/library/csv.html)


Put your csv data into typed model
```python
from typed_csv import TypedReader, BaseModel


class UsersModel(BaseModel):
    name: str
    phone: int


with open("users.csv") as csvfile:
    typed_reader = TypedReader(csvfile, delimiter=";", model=UsersModel)
    for row in typed_reader:
        print(row.name)
```