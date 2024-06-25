# LIBRARY-API

The library-api is a RESTful API that provides endpoints for managing a library system. It allows users to perform operations such as adding books, borrowing books, making reservations, writing reviews, and retrieving statistics. The API is built using Python and Flask framework, and it utilizes MongoDB as the database for storing and retrieving data. The project follows a modular structure, with separate modules for services, models, and routes. The services module contains the business logic for each feature, the models module defines the data models, and the routes module handles the HTTP endpoints.


## Repository structure

```
library-api/
├── app.py
├── config.py
├── conftest.py
├── db.py
├── models
│   ├── book.py
│   ├── loan.py
│   ├── reservation.py
│   ├── review.py
│   └── user.py
├── requirements.txt
├── roles.py
├── routes
│   ├── auth.py
│   ├── books.py
│   ├── loans.py
│   ├── reservations.py
│   ├── reviews.py
│   ├── statistics.py
│   └── users.py
├── services
│   ├── books_service.py
│   ├── loans_service.py
│   ├── reservations_service.py
│   ├── statistics_service.py
│   └── users_service.py
└── tests
    ├── test_auth.py
    ├── test_books.py
    ├── test_loans.py
    ├── test_mongodb_connection.py
    ├── test_reservations.py
    ├── test_reviews.py
    ├── test_statistics.py
    └── test_users.py
```

## Modules

- services
- models
- routes

## Getting Started

### Installation

Clone the library-api repository:

```
git clone https://github.com/dezmerek/library-api
```

Change to the project directory:

```
cd library-api
```

Install the dependencies:

```
pip install -r requirements.txt
```

### Running library-api

Use the following command to run library-api:

```
python main.py
```

### Tests

To execute tests, run:

```
pytest
```

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
MONGO_URI=
```

Make sure to replace the values with your own database configuration.
