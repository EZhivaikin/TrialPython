from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, conlist, constr, conint

from app.schemas.category import Category
from app.settings import MIN_CATEGORIES_COUNT, MAX_CATEGORIES_COUNT


class ProductBase(BaseModel):
	name: constr(min_length=1, max_length=50)
	rating: float
	featured: Optional[bool]
	expiration_date: datetime
	items_in_stock: conint(gt=0, lt=9223372036854775807)
	receipt_date: datetime


class ProductInDB(ProductBase):
	id: int
	created_at: datetime


class ProductCreate(ProductBase):
	brand_id: int
	categories: conlist(int, min_items=MIN_CATEGORIES_COUNT, max_items=MAX_CATEGORIES_COUNT)


class ProductUpdate(ProductCreate):
	pass


class BrandInfo(BaseModel):
	id: int
	name: str
	country_code: str


class Product(ProductInDB):
	brand: BrandInfo
	categories: List[Category]


class ProductWithBrandId(ProductBase):
	brand_id: int
	categories: List[Category]
