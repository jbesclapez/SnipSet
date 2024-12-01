from app import create_app, db
from app.models.models import Role

# Create the Flask app instance
app = create_app()

# Use the app context to initialize the database and add roles
with app.app_context():
    # Create all tables
    db.create_all()

    # Add predefined roles if not already present
    try:
        # Use db.session.query explicitly to avoid issues with Role.query
        if not db.session.query(Role).first():
            roles = ['Administrator', 'Reviewer', 'End User']
            for role_name in roles:
                role = Role(name=role_name)
                db.session.add(role)
            db.session.commit()
            print("Predefined roles added successfully.")
        else:
            print("Roles already exist.")
    except Exception as e:
        print(f"Error initializing roles: {e}")
