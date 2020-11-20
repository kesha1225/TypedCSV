import typing

from typed_csv import TypedWriter, BaseModel


class MyModel(BaseModel):
    keywords: typing.List[str]
    price: int
    product_name: str


with open("my_ikea.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = TypedWriter(csvfile, model=MyModel, extrasaction="raise")

    writer.writeheader()

    writer.writerow(MyModel(keywords=["kw1", "kw2"], price=123, product_name="ОПЛЕВ"))
    writer.writerow(MyModel(keywords=["kw3", "kw4"], price=456, product_name="БАН"))

    # or
    # writer.writerows(
    #     [
    #         MyModel(keywords=["kw1", "kw2"], price=123, product_name="ОПЛЕВ"),
    #         MyModel(keywords=["kw3", "kw4"], price=456, product_name="БАН"),
    #     ]
    # )
