from typing import List

from pydantic import BaseModel

from app.schemas.product import ProductWithBrandId


class BrandBase(BaseModel):
	name: str
	country_code: str


class BrandInDB(BrandBase):
	id: int




class Brand(BrandInDB):
	products: List[ProductWithBrandId]
