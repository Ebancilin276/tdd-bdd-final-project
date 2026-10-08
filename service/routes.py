"""
Product Routes - RESTful API endpoints for Product resources
"""
from flask import jsonify, request, abort
from service import app, db
from service.models import Product, Category


######################################################################
# Health Endpoint
######################################################################
@app.route("/health")
def healthcheck():
    """Health check endpoint"""
    return jsonify(status=200, message="OK"), 200


######################################################################
# Home Page
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = f"/products/{product.id}"
    return jsonify(message), 201, {"Location": location_url}


######################################################################
# READ A PRODUCT (Task 4a)
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with id '{product_id}' was not found.")
    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), 200


######################################################################
# UPDATE AN EXISTING PRODUCT (Task 4b)
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), 200


######################################################################
# DELETE A PRODUCT (Task 4c)
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based on its id
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", 204


######################################################################
# LIST ALL PRODUCTS (Task 4d)
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """
    List all Products
    This endpoint will list all Products, with optional filtering
    by name, category, or availability
    """
    app.logger.info("Request to list Products...")
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        app.logger.info("Filtering by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Filtering by category: %s", category)
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        app.logger.info("Filtering by availability: %s", available)
        available_value = available.lower() in ("true", "yes", "1")
        products = Product.find_by_availability(available_value)
    else:
        app.logger.info("Returning all products")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), 200


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            415,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        415,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(404)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=404, error="Not Found", message=message),
        404,
    )


@app.errorhandler(415)
def mediatype_not_supported(error):
    """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=415, error="Unsupported media type", message=message),
        415,
    )
