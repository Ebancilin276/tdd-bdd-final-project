# TDD and BDD Final Project

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

This project demonstrates **Test Driven Development (TDD)** and **Behavior Driven Development (BDD)** practices for a RESTful Product Catalog service built with Python and Flask.

The project implements a complete REST API for managing products with full CRUD operations and query capabilities, along with comprehensive test suites using both TDD (pytest) and BDD (behave) approaches.

## Project Structure

```
tdd-bdd-final-project/
├── service/                    # Application source code
│   ├── __init__.py             # Flask app initialization
│   ├── models.py               # Product data model (SQLAlchemy)
│   └── routes.py               # REST API routes
├── tests/                      # TDD test suite
│   ├── __init__.py
│   ├── factories.py            # Test data factory (factory_boy)
│   ├── test_models.py          # Model unit tests
│   └── test_routes.py          # API route integration tests
├── features/                   # BDD test suite
│   ├── environment.py          # Behave environment setup
│   ├── products.feature        # Gherkin feature scenarios
│   └── steps/                  # Step definitions
│       ├── load_steps.py       # Background data loading steps
│       └── web_steps.py        # Web interaction steps
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Programming language |
| **Flask** | Web framework |
| **SQLAlchemy** | ORM for database operations |
| **pytest** | TDD test framework |
| **factory_boy** | Test data generation |
| **behave** | BDD test framework |
| **Gherkin** | BDD scenario syntax |

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ebancilin276/tdd-bdd-final-project.git
cd tdd-bdd-final-project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

### Run TDD Tests (pytest)

```bash
# Run all unit and integration tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=service --cov-report=term-missing
```

### Run BDD Tests (behave)

```bash
# Run all BDD scenarios
behave features/
```

### Run All Tests

```bash
pytest tests/ -v && behave features/
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/products` | List all products |
| `GET` | `/products?name=X` | Filter products by name |
| `GET` | `/products?category=X` | Filter products by category |
| `GET` | `/products?available=X` | Filter products by availability |
| `POST` | `/products` | Create a new product |
| `GET` | `/products/<id>` | Read a single product |
| `PUT` | `/products/<id>` | Update a product |
| `DELETE` | `/products/<id>` | Delete a product |

## Product Model

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Auto-generated primary key |
| `name` | String(100) | Product name |
| `description` | String(250) | Product description |
| `price` | Numeric | Product price |
| `available` | Boolean | Product availability |
| `category` | Enum | UNKNOWN, CLOTHS, FOOD, HOUSEWARES, AUTOMOTIVE, TOOLS |

## License

Licensed under the Apache License. See [LICENSE](LICENSE) for details.

## Author

Ebancilin276
