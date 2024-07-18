# SnipSet Backend

## Setup

1. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

2. Initialize the database:

    ```sh
    docker-compose exec backend flask db init
    docker-compose exec backend flask db migrate
    docker-compose exec backend flask db upgrade
    ```

3. Access the application at `http://localhost:5000`

## Folder Structure

### backend
The root directory for the backend of the application.

- **app/**: Contains the main application code.
  - **config/**: Configuration files for the application.
    - `config.py`: Contains configuration settings such as database URI and secret keys.
  - **models/**: Database models.
    - `models.py`: Defines the SQLAlchemy models for the database schema.
  - **controllers/**: Business logic and controller code (not yet included but should be added here).
  - **routes/**: Contains the route definitions for the application.
    - `routes.py`: Defines the API endpoints and links them to controller functions.
  - `__init__.py`: Application factory to create and configure the Flask app.
  
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **directory_structure.txt**: A file listing the structure of the directory.
- **docker-compose/**: Docker compose configuration files (optional).
- **Dockerfile**: Instructions to build the Docker image for the backend service.
- **list_directory_structure_to_file.ps1**: PowerShell script to list the directory structure.
- **README.md**: Instructions and documentation for setting up and running the backend.
- **requirements.txt**: Lists the Python dependencies needed to run the application.
- **swagger.yaml**: API documentation file (if using Swagger for API documentation).
- **migrate.py**: Manages the database migrations using Flask-Migrate.
- **init_db.py**: Script to initialize the database and create tables with initial data.

## Environment Variables

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for session management
- `SECURITY_PASSWORD_SALT`: Salt for password hashing
- `RECAPTCHA_SITE_KEY`: Recaptcha site key
- `RECAPTCHA_SECRET_KEY`: Recaptcha secret key

## Running the Application

### Docker Setup

1. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

2. Initialize the database:

    ```sh
    docker-compose exec backend flask db init
    docker-compose exec backend flask db migrate
    docker-compose exec backend flask db upgrade
    ```

3. Access the application at `http://localhost:5000`

### Manual Setup (Without Docker)

1. Create a virtual environment and install dependencies:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

2. Set up environment variables in a `.env` file:

    ```plaintext
    DATABASE_URL=postgresql://snipset_user:snipset_your_password@localhost:5432/snipset_db
    SECRET_KEY=your_secret_key
    SECURITY_PASSWORD_SALT=your_password_salt
    RECAPTCHA_SITE_KEY=your_recaptcha_site_key
    RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
    ```

3. Initialize the database:

    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. Run the application:

    ```sh
    flask run
    ```

This README file provides a comprehensive guide to setting up and running the backend, as well as an explanation of the purpose of each folder and file in the backend directory structure.
