"""
Product Model - SQLAlchemy ORM Model for Products
"""
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Category(Enum):
    """Enumeration of valid Product Categories"""
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """
    Class that represents a Product

    Attributes:
        id (int): Unique identifier for the product
        name (str): Name of the product
        description (str): Description of the product
        price (Numeric): Price of the product
        available (bool): Whether the product is available
        category (Category): Category of the product
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=(Category.UNKNOWN.name)
    )

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be None to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """
        Removes a Product from the data store
        """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.description = data["description"]
            if isinstance(data["price"], (int, float, str)):
                self.price = data["price"]
            else:
                raise DataValidationError(
                    "Invalid type for [price]: " + str(type(data["price"]))
                )
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for [available]: " + str(type(data["available"]))
                )
            self.category = getattr(Category, data["category"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return db.session.query(cls).all()

    @classmethod
    def find(cls, product_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", product_id)
        return db.session.get(cls, product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return db.session.query(cls).filter(cls.name == name)

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by their availability

        Args:
            available (bool): True for products that are available
        """
        logger.info("Processing available query for %s ...", available)
        return db.session.query(cls).filter(cls.available == available)

    @classmethod
    def find_by_category(cls, category):
        """Returns all Products with the given category

        Args:
            category (Category): the category of the Products you want to match
        """
        logger.info("Processing category query for %s ...", category.name)
        return db.session.query(cls).filter(cls.category == category)

    @classmethod
    def find_by_price(cls, price):
        """Returns all Products with the given price

        Args:
            price (Decimal): the price to match
        """
        logger.info("Processing price query for %s ...", price)
        return db.session.query(cls).filter(cls.price == price)
