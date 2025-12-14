#!/usr/bin/env python3
"""
Database Migration Script
Adds admission_date column to Patient table if it doesn't exist
"""

from app import app, db
from sqlalchemy import inspect, text

def migrate_database():
    """Add admission_date column to Patient table if it doesn't exist"""
    print("🔧 Migrating database...")
    print("=" * 40)
    
    with app.app_context():
        # Check if admission_date column exists
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('patient')]
        
        if 'admission_date' in columns:
            print("✅ admission_date column already exists")
        else:
            print("📝 Adding admission_date column to Patient table...")
            try:
                # Add the column using raw SQL
                db.engine.execute(text('ALTER TABLE patient ADD COLUMN admission_date DATE'))
                db.session.commit()
                print("✅ admission_date column added successfully!")
            except Exception as e:
                print(f"❌ Error adding column: {e}")
                # Try alternative method
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text('ALTER TABLE patient ADD COLUMN admission_date DATE'))
                        conn.commit()
                    print("✅ admission_date column added successfully (alternative method)!")
                except Exception as e2:
                    print(f"❌ Error with alternative method: {e2}")
                    print("💡 You may need to delete the database and recreate it")
                    return False
        
        print("=" * 40)
        print("✅ Database migration complete!")
        return True

if __name__ == '__main__':
    migrate_database()







