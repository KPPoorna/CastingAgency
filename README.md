# CastingAgency

## Motivation for the Project

This project was developed as the capstone for the **Full Stack Web Developer Nanodegree** program by Udacity. It is designed to showcase my ability to build a complete web application. The project demonstrates key skills learned throughout the course, including building APIs with Flask, managing databases with SQLAlchemy, implementing secure authentication using Auth0 and deployment. 

## About CastingAgency

The Casting Agency API models a company dedicated to producing films while effectively managing and assigning actors to various projects. 

- **Models:**
  - **Movies**: Attributes include title and release date.
  - **Actors**: Attributes include name, age, and gender.

- **Endpoints:**
  - `GET /actors`: Retrieve a list of actors.
  - `GET /actors/<id>`: Retrieve details of a specific actor by ID.
  - `GET /movies`: Retrieve a list of movies.
  - `GET /movies/<id>`: Retrieve details of a specific movie by ID.
  - `DELETE /actors/<id>`: Remove an actor from the database.
  - `DELETE /movies/<id>`: Remove a movie from the database.
  - `POST /actors`: Add a new actor.
  - `POST /movies`: Add a new movie.
  - `PATCH /actors/<id>`: Modify an existing actor.
  - `PATCH /movies/<id>`: Modify an existing movie.

- **Roles:**
  - **Casting Assistant**: Can view actors and movies.
  - **Casting Director**: Has all the permissions of a Casting Assistant and can:
    - Add or delete an actor from the database.
    - Modify actors or movies.
  - **Executive Producer**: Has all the permissions of a Casting Director and can:
    - Add or delete a movie from the database.


## Hosted API on Render

The CastingAgency API is hosted live on Render. You can interact with the API using Postman or CURL for testing purposes. 

### API Base URL:
[https://your-app-url.onrender.com](https://castingagency-zzio.onrender.com)

Note: This app has no frontend as of now. But you can definetly use the API.

### Generate JWT Token

To authenticate and use the API, you need a valid JWT token. Follow these steps to get your token:

1. **Go to Auth0** to generate a JWT token using the following URL: 
   - [Auth0 JWT Token Generation](https://myapp-secure.us.auth0.com/authorize?audience=https://casting-agency-auth/&response_type=token&client_id=BxGTvu4My47OVTJPNi9ksg6OBNROf3qr&redirect_uri=https://127.0.0.1:8080/login-results
   )

As of now I have 3 registered users; one for each role. Use the credentials accordingly during login
- For Casting Assistant
```bash
email: ca@gmail.com
password: CA@12345
```
- For Casting Director
```bash
email: cd@gmail.com
password: CD@12345
```
- For Executive Producer
```bash
email: ep@gmail.com
password: EP@12345
```
**IMPORTANT:**
You should logout as one user before generating jwt token for another user OR you can wait till the token of the previous user expires(not recommended)

2. After successful login, you will be redirected to the specified callback URL, and the token will be in the URL parameters. The URL looks something as below:
```bash
https://127.0.0.1:8080/login-results#access_token=<access-token>&expires_in=7198&token_type=Bearer
```
Extract the `access_token` and use it in your API requests. Refer `Endpoint Documentation` of README section for more details about the endpoints.

3. You can logout using the below link:
[Logout URL](
https://myapp-secure.us.auth0.com/v2/logout?&client_id=BxGTvu4My47OVTJPNi9ksg6OBNROf3qr&redirect_uri=https://127.0.0.1:8080/logout)
.Just clicking on the link will log the user out

### Testing with Postman or cURL

Once you have the JWT token, you can use it to test the API.

- **Using Postman:**
  1. Open Postman and create a new request.
  2. In the request headers, add the following:
     - Key: `Authorization`
     - Value: `Bearer <YOUR_TOKEN_HERE>`
  3. Test any of the API endpoints (e.g., GET /actors, POST /movies).

- **Using cURL:**
  ```bash
  curl -X GET https://your-app-url.onrender.com/actors \
  -H "Authorization: Bearer <YOUR_TOKEN_HERE>"

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
    postgres://<username>:<password>@localhost:5432/testdb
    ```
- Replace `<username>` and `<password>` with your PostgresSQL database credentials
- Then just run
    ```bash
    python test_app.py
    ```

## Endpoint Documentation

### GET Endpoints

#### `GET '/actors'`

- Fetches a list of all actors.
- Returns: A JSON object containing a list of actors.
```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Actor Name",
      "age": 30,
      "gender": "Male"
    },
    ...
  ]
}
```

#### `GET '/actors/<int:actor_id>'`

- Fetches details of a specific actor by ID.
- Request Arguments: `actor_id` - integer
- Returns: An object containing the actor's details.
```json
{
    "success": true,
    "actor": {
        "id": 1,
        "name": "Actress Name",
        "age": 32,
        "gender": "Female"
    }
}
```

#### `GET '/movies'`

- Fetches a list of all movies.
- Request Arguments: None
- Returns: An object containing a list of movies.
```json
{
    "success": true,
    "movies": [
        {
            "id": 1,
            "title": "Movie Title",
            "release_date": "2023-01-01"
        },
        {
            "id": 2,
            "title": "Another Movie",
            "release_date": "2023-06-15"
        }
    ]
}
```
#### `GET '/movies/<int:movie_id>'`

- Fetches details of a specific movie by ID.
- Request Arguments: `movie_id `- integer
- Returns: An object containing the movie's details.
```json
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "Movie Title",
        "release_date": "2023-01-01"
    }
}
```

### POST Endpoints

#### `POST '/actors'`

- Creates a new actor.
- Request Body:
```json
{
  "name": "New Actor",
  "age": 28,
  "gender": "Male"
}

```
- Returns: A JSON object confirming the creation
```json
{
  "success": true,
  "created": 1,
  "actor": {
    "id": 1,
    "name": "New Actor",
    "age": 28,
    "gender": "Male"
  }
}
```
#### `POST '/movies'`

- Creates a new movie.
- Request Body:
```json
{
  "title": "New Movie",
  "release_date": "2024-01-01"
}
```
- Returns: A JSON object confirming the creation.
```json
{
  "success": true,
  "created": 1,
  "movie": {
    "id": 1,
    "title": "New Movie",
    "release_date": "2024-01-01"
  }
}
```

### PATCH Endpoints

#### `PATCH '/actors/<int:actor_id>'`

- Updates an existing actor by ID.
- Request Arguments:
  - `actor_id` - integer
- Request Body (at least one field required):
```json
{
  "name": "Updated Actor Name",
  "age": 32,
  "gender": "Non-binary"
}
```
- Returns: A JSON object with the updated actor's details.
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Updated Actor Name",
    "age": 32,
    "gender": "Non-binary"
  }
}
```

#### `PATCH '/movies/<int:movie_id>'`

- Updates an existing movie by ID.
- Request Arguments:
  - `movie_id` - integer
- Request Body (at least one field required):
```json
{
  "title": "Updated Movie Title",
  "release_date": "2024-01-02"
}
```
- Returns: A JSON object with the updated movie's details.
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Updated Movie Title",
    "release_date": "2024-01-02"
  }
}
```

### DELETE Endpoints

#### `DELETE '/actors/<int:actor_id>'`

- Deletes a specified actor using the ID of the actor.
- Request Arguments: 
  - `actor_id` - integer
- Returns: A message indicating successful deletion.
```json
{
    "success": true,
    "deleted": 1
}
```

#### `DELETE '/movies/<int:movie_id>'`

- Deletes a movie by ID.
- Request Arguments: 
  - `movie_id` - integer
- Returns: A JSON object confirming the deletion.
```json
{
  "success": true,
  "deleted": 1
}
```


