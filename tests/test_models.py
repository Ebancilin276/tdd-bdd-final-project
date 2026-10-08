"""
Test Cases for Product Model (Task 2)

Tests for CRUD operations and query methods on the Product model.
"""
import os
import logging
import unittest
from decimal import Decimal
from service import app, db
from service.models import Product, Category, DataValidationError
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

logger = logging.getLogger("flask.app")


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        with app.app_context():
            db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.app_context = app.app_context()
        self.app_context.push()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        self.app_context.pop()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_product(self, count=1):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            product = ProductFactory()
            product.id = None
            product.create()
            products.append(product)
        return products

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.find(product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    # ------------------------------------------------------------------
    # Task 2a: READ a Product
    # ------------------------------------------------------------------
    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch the product back from the database
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    # ------------------------------------------------------------------
    # Task 2b: UPDATE a Product
    # ------------------------------------------------------------------
    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        original_id = product.id
        # Change a field and save
        product.description = "Updated description for testing"
        product.update()
        # Fetch it back and verify the update
        updated = Product.find(original_id)
        self.assertEqual(updated.id, original_id)
        self.assertEqual(updated.description, "Updated description for testing")

    def test_update_a_product_without_id(self):
        """It should not Update a Product with no id"""
        product = ProductFactory()
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    # ------------------------------------------------------------------
    # Task 2c: DELETE a Product
    # ------------------------------------------------------------------
    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        self.assertEqual(len(Product.all()), 1)
        # Delete the product and make sure it is gone
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    # ------------------------------------------------------------------
    # Task 2d: LIST ALL Products
    # ------------------------------------------------------------------
    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(len(products), 0)
        # Create 5 Products
        self._create_product(5)
        # Verify there are now 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    # ------------------------------------------------------------------
    # Task 2e: FIND BY NAME
    # ------------------------------------------------------------------
    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = self._create_product(5)
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    # ------------------------------------------------------------------
    # Task 2f: FIND BY CATEGORY
    # ------------------------------------------------------------------
    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = self._create_product(10)
        category = products[0].category
        count = len([p for p in products if p.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    # ------------------------------------------------------------------
    # Task 2g: FIND BY AVAILABILITY
    # ------------------------------------------------------------------
    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = self._create_product(10)
        available = products[0].available
        count = len([p for p in products if p.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_find_by_price(self):
        """It should Find Products by Price"""
        products = self._create_product(5)
        price = products[0].price
        count = len([p for p in products if p.price == price])
        found = Product.find_by_price(price)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.price, price)

    def test_serialize_a_product(self):
        """It should Serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertIsNotNone(data)
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("price", data)
        self.assertIn("available", data)
        self.assertIn("category", data)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["price"], str(product.price))
        self.assertEqual(data["available"], product.available)
        self.assertEqual(data["category"], product.category.name)

    def test_deserialize_a_product(self):
        """It should Deserialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.available, data["available"])
        self.assertEqual(product.category.name, data["category"])

    def test_deserialize_missing_data(self):
        """It should not Deserialize a Product with missing data"""
        data = {"id": 1, "name": "Test"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not Deserialize a Product with bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not Deserialize a Product with bad available attribute"""
        data = ProductFactory().serialize()
        data["available"] = "true"  # Should be a boolean
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_category(self):
        """It should not Deserialize a Product with bad category attribute"""
        data = ProductFactory().serialize()
        data["category"] = "invalid"  # Invalid category
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)


######################################################################
#  M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
