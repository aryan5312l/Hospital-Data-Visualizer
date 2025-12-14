"""
Test script to import patients from CSV
Run this to verify the import is working correctly
"""
import sys
import os

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, import_patients_from_csv, Patient, User

with app.app_context():
    # Count existing patients
    existing_count = Patient.query.count()
    print(f"Existing patients in database: {existing_count}")
    
    # Import patients
    print("\nImporting patients from dummy_patients.csv...")
    imported = import_patients_from_csv('dummy_patients.csv')
    
    # Count after import
    new_count = Patient.query.count()
    print(f"\nPatients after import: {new_count}")
    print(f"New patients imported: {imported}")
    print(f"Total patients now: {new_count}")


