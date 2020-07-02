from pydantic import BaseModel


class CategoryBase(BaseModel):
	name: str


class CategoryInDB(CategoryBase):
	id: int


class Category(CategoryInDB):
	pass
