Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description        | price  | available | category   |
        | Hat        | A red fedora       | 59.95  | True      | CLOTHS     |
        | Shoes      | Blue shoes         | 120.50 | False     | CLOTHS     |
        | Big Mac    | 1/4 lb burger      | 5.99   | True      | FOOD       |
        | Sheets     | Queen size sheets  | 63.50  | True      | HOUSEWARES |
        | Hammer     | A steel hammer     | 11.99  | True      | TOOLS      |

# ------------------------------------------------------------------
# Scenario 6a: READING a Product
# ------------------------------------------------------------------
Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "CLOTHS" in the "Category" dropdown

# ------------------------------------------------------------------
# Scenario 6b: UPDATING a Product
# ------------------------------------------------------------------
Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I change "Name" to "Fedora"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Fedora" in the "Name" field

# ------------------------------------------------------------------
# Scenario 6c: DELETING a Product
# ------------------------------------------------------------------
Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Hat" in the results

# ------------------------------------------------------------------
# Scenario 6d: LISTING ALL PRODUCTS
# ------------------------------------------------------------------
Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should see "Hammer" in the results

# ------------------------------------------------------------------
# Scenario 6e: Searching by Category
# ------------------------------------------------------------------
Scenario: Search Products by Category
    When I visit the "Home Page"
    And I select "CLOTHS" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results
    And I should not see "Hammer" in the results

# ------------------------------------------------------------------
# Scenario 6f: Searching by Availability
# ------------------------------------------------------------------
Scenario: Search Products by Availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should see "Hammer" in the results
    And I should not see "Shoes" in the results

# ------------------------------------------------------------------
# Scenario 6g: Searching by Name
# ------------------------------------------------------------------
Scenario: Search Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results
