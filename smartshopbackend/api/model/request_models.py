

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
    catagory: str
    description: str


@attr.define
class UserLoginRequest(FilteredDictConvertible):
    user: str
    password: str


@attr.define
class CartListRequest(FilteredDictConvertible):
    products: str
    quantity: int
    user: Optional[str] = ""
