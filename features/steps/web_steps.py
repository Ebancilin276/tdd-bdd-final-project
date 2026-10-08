"""
Web Steps - Step definitions for browser/UI interactions (Task 7)

This module provides step definitions that simulate web interactions
for BDD testing. Steps handle button clicks, field setting/reading,
result verification, and message checking.
"""
import requests
from behave import when, then


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.resp = requests.get(context.base_url)
    assert context.resp.status_code == 200


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a form field value"""
    element_id = element_name.lower().replace(" ", "_")
    context.data[element_id] = text_string


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change an existing form field value"""
    element_id = element_name.lower().replace(" ", "_")
    context.data[element_id] = text_string


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select a value from a dropdown"""
    element_id = element_name.lower().replace(" ", "_")
    context.data[element_id] = text


# ------------------------------------------------------------------
# Task 7a: Button Click
# ------------------------------------------------------------------
@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button to perform an action via the REST API"""
    button_lower = button.lower()
    base = f"{context.base_url}/products"

    if button_lower == "search":
        # Build query string from context data
        params = {}
        if "name" in context.data and context.data["name"]:
            params["name"] = context.data["name"]
        elif "category" in context.data and context.data["category"]:
            params["category"] = context.data["category"]
        elif "available" in context.data and context.data["available"]:
            params["available"] = context.data["available"]
        context.resp = requests.get(base, params=params)
        assert context.resp.status_code == 200
        context.search_results = context.resp.json()
        context.message = "Success"

    elif button_lower == "clear":
        context.data = {}
        context.product_id = getattr(context, "clipboard", "")
        context.message = ""

    elif button_lower == "create":
        payload = {
            "name": context.data.get("name", ""),
            "description": context.data.get("description", ""),
            "price": context.data.get("price", "0"),
            "available": context.data.get("available", "True") in ("True", "true"),
            "category": context.data.get("category", "UNKNOWN"),
        }
        context.resp = requests.post(base, json=payload)
        assert context.resp.status_code == 201
        context.message = "Success"
        context.data = context.resp.json()

    elif button_lower == "retrieve":
        product_id = context.data.get("id", "")
        context.resp = requests.get(f"{base}/{product_id}")
        assert context.resp.status_code == 200
        context.data = context.resp.json()
        context.message = "Success"

    elif button_lower == "update":
        product_id = context.data.get("id", "")
        payload = {
            "name": context.data.get("name", ""),
            "description": context.data.get("description", ""),
            "price": context.data.get("price", "0"),
            "available": context.data.get("available", True),
            "category": context.data.get("category", "UNKNOWN"),
        }
        # Handle available being a string
        if isinstance(payload["available"], str):
            payload["available"] = payload["available"] in ("True", "true")
        context.resp = requests.put(f"{base}/{product_id}", json=payload)
        assert context.resp.status_code == 200
        context.data = context.resp.json()
        context.message = "Success"

    elif button_lower == "delete":
        product_id = context.data.get("id", "")
        context.resp = requests.delete(f"{base}/{product_id}")
        assert context.resp.status_code == 204
        context.message = "Product has been Deleted!"
        context.data = {}

    else:
        context.message = f"Unknown button: {button}"


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a field value to the clipboard"""
    element_id = element_name.lower().replace(" ", "_")
    context.clipboard = context.data.get(element_id, "")


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste the clipboard value into a field"""
    element_id = element_name.lower().replace(" ", "_")
    context.data[element_id] = context.clipboard


# ------------------------------------------------------------------
# Task 7b: Verify a specific name/text is present
# ------------------------------------------------------------------
@then('I should see "{text}" in the "{element_name}" field')
def step_impl(context, text, element_name):
    """Verify that a field contains the expected value"""
    element_id = element_name.lower().replace(" ", "_")
    found = str(context.data.get(element_id, ""))
    assert text in found, f"Expected '{text}' in '{element_name}' field, but got '{found}'"


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Verify that a dropdown contains the expected value"""
    element_id = element_name.lower().replace(" ", "_")
    found = str(context.data.get(element_id, ""))
    assert text in found, f"Expected '{text}' in '{element_name}' dropdown, but got '{found}'"


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Verify that a specific product name appears in the search results"""
    found = False
    for product in context.search_results:
        if product["name"] == name:
            found = True
            break
    assert found, f"Expected '{name}' in the results but it was not found"


# ------------------------------------------------------------------
# Task 7c: Verify a specific name/text is NOT present
# ------------------------------------------------------------------
@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Verify that a specific product name does NOT appear in the results"""
    found = False
    for product in context.search_results:
        if product["name"] == name:
            found = True
            break
    assert not found, f"'{name}' should not be in the results but it was found"


# ------------------------------------------------------------------
# Task 7d: Verify a specific message is present
# ------------------------------------------------------------------
@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify that the expected message is displayed"""
    assert context.message == message, (
        f"Expected message '{message}', but got '{context.message}'"
    )
