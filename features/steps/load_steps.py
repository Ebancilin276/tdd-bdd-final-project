"""
Load Steps - Step definitions for loading background product data (Task 5)

This module provides the step definition for loading product data
from the Background section of the BDD feature file.
"""
import requests
from behave import given


@given('the following products')
def step_impl(context):
    """Load the products from the Background table into the service"""
    # First, delete all existing products (clean state)
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == 200

    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert context.resp.status_code == 204

    # Now load the products from the table
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"] in ("True", "true", "1", "yes"),
            "category": row["category"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == 201
