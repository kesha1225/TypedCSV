import typing

from typed_csv import TypedReader, BaseModel


class MyModel(BaseModel):
    keywords: typing.List[str]
    price: int
    product_name: str


with open("ikea.csv", encoding="utf-8") as csvfile:

    # First colums keywords looks like a 'МОРУМ, Ковер, безворсовый;' then list_delimiter=","

    typed_reader = TypedReader(
        csvfile, delimiter=";", model=MyModel, list_delimiter=","
    )
    for row in typed_reader:
        print(row.keywords)
