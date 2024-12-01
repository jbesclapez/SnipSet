from app import create_app
import logging
import os
import app.error_handlers  # Ensure this import is here to register the error handlers

# Configure logging
logging.basicConfig(level=logging.DEBUG if os.getenv('FLASK_ENV') == 'development' else logging.INFO)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
