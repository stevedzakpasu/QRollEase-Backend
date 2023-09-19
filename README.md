# QRollEase API

This is the backend service for [QRollEase](https://github.com/stevedzakpasu/QRollEase-Mobile).
It is a mobile application I built as part of my senior year final project to solve issues with the current attendance management system at the University of Ghana.
This Python-based API is built with FastAPI, SQLModel, and PostgreSQL to enable efficient attendance tracking for students and lecturers using QR codes and geolocation.

## Getting Started

### Prerequisites

Before running this API, ensure you have the following prerequisites installed on your system:

- Python 3.8+
- PostgreSQL

### Installation

1. Clone this repository to your local machine:

   `git clone https://github.com/stevedzakpasu/QRollEase-Backend.git`

2. Navigate to the project directory:
   `cd QRollEase-Backend`

3. Create a virtual environment, activate it and install the required libraries:
   `pip install -r requirements.txt`

4. Create a .env file in the project root directory and configure the database connection URL and other necessary environment variables:

   ```
   DB_URL = postgresql://username:password@localhost/dbname
   MAIL_PASSWORD =
   SECRET_KEY =
   SUPERUSER_PASSWORD =
   SUPERUSER_EMAIL =
   ```

5. Apply database migrations:

   `pipenv run alembic upgrade head`

6. Start the FastAPI server:
   `pipenv run uvicorn main:app --reload`

## Data Models

You can find the data model definitions in the app/models directory.

## Database Setup

This API uses PostgreSQL as the database. Ensure that you have set up your PostgreSQL server and configured the DB_URL in the .env file as mentioned in the installation steps.

## Deployment

You can deploy your own instance of this API using your favorite hosting platform.

## Authentication

This API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you need to include an Authorization header with a valid JWT token. You can obtain a token by registering and logging in through the authentication endpoints.

## Documentation

You can locate the complete documentation for the web service to view all endpoints [here](https://qrollease-api-112d897b35ef.herokuapp.com/docs).

Or using the running local server:
<http://localhost:8000/docs>

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Screenshots

![Screenshot](/screenshots/screenshot1.png)
![Screenshot](/screenshots/screenshot2.png)
