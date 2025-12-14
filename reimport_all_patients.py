"""
Script to clear existing patients and re-import all from CSV
This ensures all 1,200 patients are imported
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, import_patients_from_csv, Patient, User, LabReport, VitalSigns, MedicalNote, Appointment

with app.app_context():
    print("Clearing existing patient data...")
    
    # Delete dependent records first
    LabReport.query.delete()
    VitalSigns.query.delete()
    MedicalNote.query.delete()
    Appointment.query.delete()
    
    # Delete patients and their user accounts
    patient_users = User.query.join(Patient, Patient.user_id == User.id).all()
    patient_count = Patient.query.count()
    Patient.query.delete()
    
    for u in patient_users:
        db.session.delete(u)
    
    db.session.commit()
    print(f"Deleted {patient_count} existing patients and their user accounts")
    
    print("\nImporting all patients from dummy_patients.csv...")
    print("This may take 1-2 minutes for 1,200 patients...")
    
    imported = import_patients_from_csv('dummy_patients.csv')
    
    # Verify
    final_count = Patient.query.count()
    print(f"\n✅ Import complete!")
    print(f"   Imported: {imported} patients")
    print(f"   Total in database: {final_count} patients")
    
    if final_count < 1200:
        print(f"\n⚠️  Warning: Expected 1,200 patients but only {final_count} were imported")
        print("   This might be due to errors during import. Check the output above for error messages.")
    else:
        print(f"\n✅ Success! All patients imported successfully.")



