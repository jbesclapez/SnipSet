from app import create_app
from app.models import db, Role

app = create_app()

with app.app_context():
    db.create_all()

    # Insert predefined roles
    if not Role.query.first():
        roles = ['Administrator', 'Reviewer', 'End User']
        for role in roles:
            db.session.add(Role(name=role))
        db.session.commit()
