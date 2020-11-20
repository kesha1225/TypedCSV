# TypedCsv

Typed extension for default [csv library](https://docs.python.org/3/library/csv.html)

Installation
```
pip install typed_csv
```


Put your csv data into typed model
```python
from typed_csv import TypedReader, BaseModel


class UsersModel(BaseModel):
    name: str
    phone: int


with open("users.csv") as csvfile:
    typed_reader = TypedReader(csvfile, delimiter=";", model=UsersModel)
    for row in typed_reader:
        print(type(row))  # <class '__main__.UsersModel'>
        print(row.name)
```


Put your typed model into csv file

```python
from typed_csv import TypedWriter, BaseModel


class UsersModel(BaseModel):
    name: str
    phone: int


with open("users.csv") as csvfile:
    writer = TypedWriter(csvfile, model=UsersModel)
    writer.writeheader()

    writer.writerow(UsersModel(name="Kolya", phone=89041588888))
    writer.writerow(UsersModel(name="Antosha", phone=89123456789))
```
