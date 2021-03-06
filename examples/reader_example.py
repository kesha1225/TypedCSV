import typing
import pydantic

from typed_csv import TypedReader, BaseModel


class MyModel(BaseModel):
    keywords: typing.List[str]
    price: typing.Optional[int]  # if price not set
    product_name: str = pydantic.Field(alias="product-name")


with open("ikea.csv", encoding="utf-8") as csvfile:

    # First colums keywords looks like a 'МОРУМ, Ковер, безворсовый;' then list_delimiter=","

    typed_reader = TypedReader(
        csvfile, delimiter=";", model=MyModel, list_delimiter=","
    )
    for row in typed_reader:
        print(row)
        print(row.keywords)
