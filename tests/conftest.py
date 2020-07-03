import pytest
from app import create_app, db as the_db

# Initialize the Flask-App with test-specific settings
from app.models.products import Product
from app.services.products_service import ProductService
from tests.factories import ProductFactory, BrandFactory, CategoryFactory

the_app = create_app(dict(
	TESTING=True,  # Propagate exceptions
	LOGIN_DISABLED=False,  # Enable @register_required
	MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
	SERVER_NAME='localhost',  # Enable url_for() without request context
	SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
	WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
))

# Setup an application context (since the tests run outside of the webserver context)
the_app.app_context().push()

# Create and populate roles and users tables
from app.commands.init_db import init_db

init_db()


@pytest.fixture(scope='session')
def app():
	""" Makes the 'app' parameter available to test functions. """
	return the_app


@pytest.fixture(scope='session')
def db():
	""" Makes the 'db' parameter available to test functions. """
	return the_db


@pytest.fixture(scope='function')
def session(db, request):
	"""Creates a new database session for a test."""
	connection = db.engine.connect()
	transaction = connection.begin()

	options = dict(bind=connection, binds={})
	session = db.create_scoped_session(options=options)

	db.session = session

	def teardown():
		transaction.rollback()
		connection.close()
		session.remove()

	request.addfinalizer(teardown)
	return session


@pytest.fixture(scope='function')
def product_request():
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
	return request_json


@pytest.fixture
def client(app):
	with app.test_client() as client:
		yield client
