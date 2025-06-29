

import attr
from .base import FilteredDictConvertible
from typing import Optional

@attr.define
class Catagory(FilteredDictConvertible):
    name: str


@attr.define
class Product(FilteredDictConvertible):
    name: str
    price: int
    catagory: Catagory
    description: str

    def __attrs_post_init__(self):
        if isinstance(self.catagory, dict):
            self.catagory = Catagory.from_dict(self.catagory)


@attr.define
class UserLoginRequest(FilteredDictConvertible):
    user: str
    password: str


@attr.define
class CartListRequest(FilteredDictConvertible):
    products: Product
    quantity: int
    # total_price : Optional[int]

    def __attrs_post_init__(self):
        if isinstance(self.products, dict):
            self.products = Product.from_dict(self.products)
