import datetime

import factory.alchemy
import factory.fuzzy
from factory.compat import UTC

from app import db
from app.models.products import Brand, Category, Product


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		abstract = True
		sqlalchemy_session = db.session


class BrandFactory(BaseFactory):
	class Meta:
		model = Brand

	name = factory.fuzzy.FuzzyText()
	country_code = factory.fuzzy.FuzzyText(length=2)


class CategoryFactory(BaseFactory):
	class Meta:
		model = Category

	name = factory.fuzzy.FuzzyText()


class ProductFactory(BaseFactory):
	class Meta:
		model = Product

	name = factory.fuzzy.FuzzyText()
	rating = factory.fuzzy.FuzzyInteger(0, 10)
	featured = factory.fuzzy.FuzzyChoice(choices=[True, False])

	expiration_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=UTC))

	brand_id = factory.SubFactory(BrandFactory)
	categories = factory.List([factory.SubFactory(CategoryFactory) for _ in range(5)])
	items_in_stock = factory.fuzzy.FuzzyInteger(0, 10)
	receipt_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=UTC))
