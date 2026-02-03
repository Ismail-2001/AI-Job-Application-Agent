from app import app, db
from models import User, MasterProfile, JobApplication
import os

def check_and_fix_db():
    print("🛠️ Checking database structure...")
    with app.app_context():
        try:
            # Check if JobApplication has cv_path
            db.session.query(JobApplication).first()
            print("✅ Database connection successful.")
            
            # Use SQLAlchemy reflection to check columns
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('job_application')]
            
            required = ['cv_path', 'cl_path', 'match_score']
            missing = [r for r in required if r not in columns]
            
            if missing:
                print(f"⚠️ Missing columns: {missing}. Recreating database for safety...")
                db.drop_all()
                db.create_all()
                from werkzeug.security import generate_password_hash
                if not User.query.filter_by(email='user@example.com').first():
                    user = User(email='user@example.com', password_hash=generate_password_hash('password'))
                    db.session.add(user)
                    db.session.commit()
                print("✅ Database recreated with new schema.")
            else:
                print("✅ All required columns present.")
                
        except Exception as e:
            print(f"❌ Error checking DB: {e}. Attempting to create all...")
            db.create_all()
            print("✅ Database created.")

if __name__ == "__main__":
    check_and_fix_db()
