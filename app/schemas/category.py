from pydantic import BaseModel, constr


class CategoryBase(BaseModel):
	name: constr(min_length=1, max_length=50)


class CategoryInDB(CategoryBase):
	id: int


class Category(CategoryInDB):
	pass
