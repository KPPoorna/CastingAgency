# CastingAgency

## Motivation for the Project

This project was developed as the capstone for the **Full Stack Web Developer Nanodegree** program by Udacity. It is designed to showcase my ability to build a complete web application. The project demonstrates key skills learned throughout the course, including building APIs with Flask, managing databases with SQLAlchemy, implementing secure authentication using Auth0 and deployment. 

## Getting Started

To get a copy of the project up and running on your local machine, follow these steps:

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.6 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

#### Key dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KPPoorna/CastingAgency.git
   ```
2. **Navigate to the project directory:**
    ```bash
    cd CastingAgency
    ```
3. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
4. **Activate the virtual environment**
    ```bash
    venv\Scripts\activate
    ```
5. **Install the required packages**
   ```bash
    pip install -r requirements.txt
    ```
6. **Set up environmental variables**
    - Make sure to create a database named `castingagency` in your PostgreSQL server.
    - Go to the .env file, change the value of `DATABASE_URI` to 
        ```bash
        postgres://<username>:<password>@localhost:5432/castingagency
        ```
    - Replace `<username>` and `<password>` with your PostgresSQL database credentials

### Running the server

To run the server locally, use the below commands
```bash
set FLASK_APP=app.py
set FLASK_DEBUG=true
python app.py
```

### Testing

- Make sure to create a database named `testdb` in your PostgreSQL server.
- Go to the .env file, change the value of `TEST_DATABASE_URI` to 
    ```bash
    postgres://<username>:<password>@localhost:5432/castingagency
    ```
- Replace `<username>` and `<password>` with your PostgresSQL database credentials
- Then just run
    ```bash
    python test_app.py
    ```

