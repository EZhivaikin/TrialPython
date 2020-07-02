from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, abort
from flask_pydantic import validate
from sqlalchemy.orm.exc import NoResultFound

from app import services
from app.models.products import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.settings import TIME_FORMAT

products_blueprint = Blueprint('products', __name__)


@products_blueprint.route('/products/', methods=['GET'])
def get_products():
	return jsonify({
		'results': [p.serialized for p in Product.query.all()]
	})


@products_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id: int):
	try:
		product = services.product.get_product(id)
	except NoResultFound as error:
		return error.args[0], 404
	return jsonify(product.serialized)


@products_blueprint.route('/products', methods=['POST'])
@validate(body=ProductCreate)
def create_product():
	product_dict = request.get_json()
	try:
		validate_expiration_date(product_dict)
	except ValueError as error:
		return error.args[0], 400
	try:
		new_product = services.product.create_product(product_dict)
	except NoResultFound as error:
		return error.args[0], 404
	return jsonify(new_product.serialized)


@products_blueprint.route('/products/<int:id>', methods=['PUT'])
@validate(body=ProductUpdate)
def update_product(id: int):
	product_dict = request.get_json()
	try:
		validate_expiration_date(product_dict)
	except ValueError as error:
		return error.args[0], 400

	try:
		updated_product = services.product.update_product(id, product_dict)
	except NoResultFound as error:
		return error.args[0], 404
	return jsonify(updated_product.serialized)


@products_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id: int):
	try:
		removed_product = services.product.delete_product(id)
	except NoResultFound as error:
		return error.args[0], 404
	return jsonify(removed_product.serialized)


def validate_expiration_date(product_dict):
	if product_dict['expiration_date'] is not None:
		expiration_date = datetime.strptime(product_dict['expiration_date'], TIME_FORMAT)
		min_date = datetime.now() + timedelta(days=30)
		if expiration_date < min_date:
			raise ValueError({'error': 'Expiration date lower than 30 days since now', 'field': 'expiration_date'})