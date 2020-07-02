from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.products import Product, Brand, Category
from datetime import datetime

from app.settings import TIME_FORMAT


class ProductService:
	time_format = "%Y-%m-%dT%H:%M:%SZ"

	def get_product(self, id: int):
		product = Product.query.get(id)
		if product is None:
			raise NoResultFound({'error': 'Product not found', 'field': 'id'})
		return product

	def create_product(self, new_product_dict: dict):
		brand = Brand.query.get(new_product_dict.get('brand_id'))
		if brand is None:
			raise NoResultFound({'error': 'Brand not found', 'field': 'brand_id'})

		new_product_dict = self.__normalize_json(new_product_dict)
		new_product = Product(**new_product_dict)

		if new_product.rating > 8:
			new_product.featured = True
		db.session.add(new_product)
		db.session.commit()
		db.session.refresh(new_product)
		return new_product

	def update_product(self, id, update_product_dict: dict):
		product = Product.query.get(id)
		if product is None:
			raise NoResultFound({'error': 'Product not found', 'field': 'id'})
		brand = Brand.query.get(update_product_dict.get('brand_id'))
		if brand is None:
			raise NoResultFound({'error': 'Brand not found', 'field': 'brand_id'})


		update_product_dict = self.__normalize_json(update_product_dict)
		for field in product.__dict__:
			if field in update_product_dict and (not update_product_dict[field] is None):
				setattr(product, field, update_product_dict[field])

		if product.rating > 8:
			product.featured = True
		db.session.add(product)
		db.session.commit()
		db.session.refresh(product)
		return product

	def delete_product(self, id: int):
		product = Product.query.get(id)
		if product is None:
			raise NoResultFound({'error': 'Product not found', 'field': 'id'})
		db.session.delete(product)
		db.session.commit()
		return product

	def __normalize_json(self, obj):
		obj['receipt_date'] = datetime.strptime(obj['receipt_date'], TIME_FORMAT)
		obj['expiration_date'] = datetime.strptime(obj['expiration_date'], TIME_FORMAT)
		categories = obj.get('categories')
		if categories:
			obj['categories'] = Category.query.filter(Category.id.in_(categories)).all()

		return obj


product = ProductService()
