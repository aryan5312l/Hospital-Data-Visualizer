#!/usr/bin/env python3
"""
Re-import Patients Script
Deletes existing patients and re-imports from dummy_patients.csv with admission dates
"""

from app import app, db, Patient, User, LabReport, VitalSigns, MedicalNote, Appointment
from app import import_patients_from_csv, _delete_all_patient_data

def reimport_patients():
    """Delete existing patients and re-import from CSV"""
    print("🔄 Re-importing patients...")
    print("=" * 40)
    
    with app.app_context():
        # Count existing patients
        existing_count = Patient.query.count()
        print(f"📊 Found {existing_count} existing patients")
        
        if existing_count > 0:
            print("🗑️  Deleting existing patient data...")
            _delete_all_patient_data()
            print("✅ Existing patient data deleted")
        
        # Import from CSV
        print("📥 Importing patients from dummy_patients.csv...")
        imported = import_patients_from_csv('dummy_patients.csv')
        print(f"✅ Imported {imported} patients")
        
        # Verify admission dates
        patients_with_dates = Patient.query.filter(Patient.admission_date.isnot(None)).count()
        print(f"📅 Patients with admission dates: {patients_with_dates}")
        
        if patients_with_dates > 0:
            # Show sample dates
            sample_patients = Patient.query.filter(Patient.admission_date.isnot(None)).limit(5).all()
            print("\n📋 Sample admission dates:")
            for p in sample_patients:
                print(f"   - {p.first_name} {p.last_name}: {p.admission_date}")
        
        print("=" * 40)
        print("✅ Re-import complete!")

if __name__ == '__main__':
    reimport_patients()







