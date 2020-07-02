from flask import url_for, json

from app.models.products import Product
from app.settings import MAX_CATEGORIES_COUNT, MIN_CATEGORIES_COUNT

from tests.factories import ProductFactory, BrandFactory, CategoryFactory


class TestProducts:
	def test_get_products(self, client):
		response = client.get(url_for("products.get_products"))
		products_dict = json.loads(response.data)
		assert response.status_code == 200
		assert 'results' in products_dict

	def test_create_product_with_not_existing_brand_should_raise_404(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': [1, 2, 3]
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 404
		assert 'error' in response_dict
		assert response_dict['field'] == 'brand_id'

	def test_create_product_not_enough_categories_should_raise_400(self, client):
		if MIN_CATEGORIES_COUNT == 0:
			assert True
			return

		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': []
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'validation_error' in response_dict

	def test_create_product_too_many_categories_should_raise_400(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': list(range(MAX_CATEGORIES_COUNT + 1))
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'validation_error' in response_dict

	def test_create_product_incorrect_expiration_date_should_raise_400(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2020-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': list(range(MAX_CATEGORIES_COUNT))
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'error' in response_dict
		assert response_dict['field'] == 'expiration_date'

	def test_update_product_with_not_existing_product_should_raise_404(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': [1, 2, 3]
		}
		response = client.put(url_for("products.update_product", id=1), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 404
		assert 'error' in response_dict
		assert response_dict['field'] == 'id'

	def test_update_product_incorrect_expiration_date_should_raise_400(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2020-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': list(range(MAX_CATEGORIES_COUNT))
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'error' in response_dict
		assert response_dict['field'] == 'expiration_date'

	def test_update_product_not_enough_categories_should_raise_400(self, client):
		if MIN_CATEGORIES_COUNT == 0:
			assert True
			return

		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': []
		}
		response = client.put(url_for("products.update_product", id=1), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'validation_error' in response_dict

	def test_update_product_too_many_categories_should_raise_400(self, client):
		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': 1,
			'categories': list(range(MAX_CATEGORIES_COUNT + 1))
		}
		response = client.put(url_for("products.update_product", id=1), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 400
		assert 'validation_error' in response_dict

	def test_delete_product_that_not_exists_should_raise_404(self, client):
		response = client.delete(url_for("products.delete_product", id=1))
		response_dict = json.loads(response.data)
		assert response.status_code == 404
		assert 'error' in response_dict
		assert response_dict['field'] == 'id'

	def test_get_product_that_not_exists_should_raise_404(self, client):
		response = client.get(url_for("products.get_product", id=1))
		response_dict = json.loads(response.data)
		assert response.status_code == 404
		assert 'error' in response_dict
		assert response_dict['field'] == 'id'

	def test_create_product_just_do_it(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)

		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': brand.id,
			'categories': [category.id]
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 200
		assert 'validation_error' not in response_dict
		assert 'error' not in response_dict
		assert response_dict['id'] is not None
		assert response_dict['name'] == request_json['name']
		assert response_dict['brand']['id'] == brand.id
		assert response_dict['categories'][0]['id'] == category.id

	def test_create_product_should_became_featured_if_rating_more_than_8(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)

		request_json = {
			'name': 'test',
			'rating': 8.5,
			'featured': False,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': brand.id,
			'categories': [category.id]
		}
		response = client.post(url_for("products.create_product"), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 200
		assert 'validation_error' not in response_dict
		assert 'error' not in response_dict
		assert response_dict['featured'] == True

	def test_update_product_just_do_it(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)
		product = ProductFactory(brand=brand, categories=[category])
		db.session.commit()
		db.session.refresh(product)

		request_json = {
			'name': 'test',
			'rating': 7,
			'featured': True,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': brand.id,
			'categories': [category.id]
		}
		response = client.put(url_for("products.update_product", id=product.id), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 200
		assert 'validation_error' not in response_dict
		assert 'error' not in response_dict
		assert response_dict['id']
		assert response_dict['name'] == request_json['name']
		assert response_dict['items_in_stock'] == request_json['items_in_stock']
		assert response_dict['rating'] == request_json['rating']

	def test_update_product_should_became_featured_if_rating_more_than_8(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)
		product = ProductFactory(brand=brand, categories=[category])
		db.session.commit()
		db.session.refresh(product)

		request_json = {
			'name': 'test',
			'rating': 8.5,
			'featured': False,
			'expiration_date': '2021-04-23T18:25:43Z',
			'items_in_stock': 10,
			'receipt_date': '2012-04-23T18:25:43Z',
			'brand_id': brand.id,
			'categories': [category.id]
		}
		response = client.put(url_for("products.update_product", id=product.id), json=request_json)
		response_dict = json.loads(response.data)
		assert response.status_code == 200
		assert 'validation_error' not in response_dict
		assert 'error' not in response_dict
		assert response_dict['featured'] == True

	def test_get_product_just_do_it(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)
		product = ProductFactory(brand=brand, categories=[category])
		db.session.commit()
		db.session.refresh(product)

		response = client.get(url_for("products.get_product", id=product.id))
		response_dict = json.loads(response.data)

		needed_product = Product.query.get(product.id)

		assert response.status_code == 200
		assert response_dict['id'] == product.id
		assert needed_product.id == product.id

	def test_delete_product_just_do_it(self, db, client):
		brand = BrandFactory()
		category = CategoryFactory()
		db.session.commit()
		db.session.refresh(category)
		db.session.refresh(brand)
		product = ProductFactory(brand=brand, categories=[category])
		db.session.commit()
		db.session.refresh(product)

		response = client.delete(url_for("products.get_product", id=product.id))
		response_dict = json.loads(response.data)

		removed_product = Product.query.get(product.id)

		assert response.status_code == 200
		assert response_dict['id'] == product.id
		assert removed_product is None
