from typing import List

from pydantic import BaseModel, constr

from app.schemas.product import ProductWithBrandId


class BrandBase(BaseModel):
	name: constr(min_length=1, max_length=50)
	country_code: constr(min_length=2, max_length=2)


class BrandInDB(BrandBase):
	id: int




class Brand(BrandInDB):
	products: List[ProductWithBrandId]
