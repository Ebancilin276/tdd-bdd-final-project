"""
Test Cases for Product Routes (Task 3)

Tests for REST API endpoints for Product resources.
"""
import os
import logging
import unittest
from decimal import Decimal
from service import app, db
from service.models import Product, Category
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

BASE_URL = "/products"
CONTENT_TYPE_JSON = "application/json"

logger = logging.getLogger("flask.app")


######################################################################
#  P R O D U C T   R O U T E   T E S T   C A S E S
######################################################################
class TestProductRoutes(unittest.TestCase):
    """Product Route Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        with app.app_context():
            db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()
        self.app_context.pop()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(
                BASE_URL,
                json=test_product.serialize(),
                content_type=CONTENT_TYPE_JSON,
            )
            self.assertEqual(
                response.status_code, 201, "Could not create test product"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "OK")

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        response = self.client.post(
            BASE_URL,
            json=test_product.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, 201)
        # Make sure Location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(Decimal(new_product["price"]), test_product.price)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["category"], test_product.category.name)

    # ------------------------------------------------------------------
    # Task 3a: READ a Product
    # ------------------------------------------------------------------
    def test_get_product(self):
        """It should Get a single Product"""
        # Create a product to read
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product that's not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    # ------------------------------------------------------------------
    # Task 3b: UPDATE a Product
    # ------------------------------------------------------------------
    def test_update_product(self):
        """It should Update an existing Product"""
        # Create a product to update
        test_product = self._create_products(1)[0]
        # Change the product data
        new_product = test_product.serialize()
        new_product["description"] = "Updated via API test"
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}",
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, 200)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "Updated via API test")

    def test_update_product_not_found(self):
        """It should not Update a Product that's not found"""
        response = self.client.put(
            f"{BASE_URL}/0",
            json={},
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------
    # Task 3c: DELETE a Product
    # ------------------------------------------------------------------
    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data), 0)
        # Make sure it is deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existing_product(self):
        """It should Delete a Product even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 204)

    # ------------------------------------------------------------------
    # Task 3d: LIST ALL Products
    # ------------------------------------------------------------------
    def test_list_all_products(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ------------------------------------------------------------------
    # Task 3e: LIST BY NAME
    # ------------------------------------------------------------------
    def test_list_by_name(self):
        """It should Query Products by Name"""
        products = self._create_products(5)
        test_name = products[0].name
        name_count = len([p for p in products if p.name == test_name])
        response = self.client.get(BASE_URL, query_string=f"name={test_name}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # Check that all returned products have the correct name
        for product in data:
            self.assertEqual(product["name"], test_name)

    # ------------------------------------------------------------------
    # Task 3f: LIST BY CATEGORY
    # ------------------------------------------------------------------
    def test_list_by_category(self):
        """It should Query Products by Category"""
        products = self._create_products(10)
        category = products[0].category
        category_count = len([p for p in products if p.category == category])
        response = self.client.get(
            BASE_URL, query_string=f"category={category.name}"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), category_count)
        for product in data:
            self.assertEqual(product["category"], category.name)

    # ------------------------------------------------------------------
    # Task 3g: LIST BY AVAILABILITY
    # ------------------------------------------------------------------
    def test_list_by_availability(self):
        """It should Query Products by Availability"""
        products = self._create_products(10)
        available = products[0].available
        available_count = len([p for p in products if p.available == available])
        response = self.client.get(
            BASE_URL, query_string=f"available={available}"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
        for product in data:
            self.assertEqual(product["available"], available)


######################################################################
#  M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
