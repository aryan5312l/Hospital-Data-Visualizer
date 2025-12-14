#!/usr/bin/env python3
"""
Generate Sample Data Script
Creates vital signs and medical notes for existing patients
"""

from app import app, db, Patient, Doctor, VitalSigns, MedicalNote
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate vital signs and medical notes for existing patients"""
    print("📊 Generating sample data...")
    print("=" * 40)
    
    with app.app_context():
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        
        if not patients:
            print("❌ No patients found. Please import patients first.")
            return
        
        if not doctors:
            print("❌ No doctors found. Please import doctors first.")
            return
        
        print(f"📋 Found {len(patients)} patients and {len(doctors)} doctors")
        
        # Generate vital signs
        vital_count = 0
        for patient in patients:
            # Generate 3-5 vital signs records per patient
            for i in range(random.randint(3, 5)):
                vital = VitalSigns(
                    patient_id=patient.id,
                    heart_rate=random.randint(60, 100),
                    blood_pressure_systolic=random.randint(110, 140),
                    blood_pressure_diastolic=random.randint(70, 90),
                    temperature=round(random.uniform(36.5, 37.5), 1),
                    weight=round(random.uniform(60, 100), 1),
                    height=round(random.uniform(150, 190), 1),
                    glucose_level=round(random.uniform(80, 120), 1),
                    recorded_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.session.add(vital)
                vital_count += 1
        
        print(f"✅ Generated {vital_count} vital signs records")
        
        # Generate medical notes with diagnoses
        diagnoses_list = [
            'Hypertension', 'Diabetes', 'Common Cold', 'Migraine', 'Arthritis',
            'Heart Disease', 'Fracture', 'Cancer', 'Skin Allergy', 'Acid Reflux',
            'Anxiety', 'Thyroid Disorder', 'Epilepsy', 'Ulcer', 'Eczema',
            'Back Pain', 'Depression', 'Gastritis', 'Headache', 'Psoriasis'
        ]
        
        note_count = 0
        for patient in patients:
            # Assign a doctor if not already assigned
            if not patient.doctor_id:
                patient.doctor_id = random.choice(doctors).id
            
            # Generate 1-3 medical notes per patient
            for i in range(random.randint(1, 3)):
                note = MedicalNote(
                    patient_id=patient.id,
                    doctor_id=patient.doctor_id or random.choice(doctors).id,
                    diagnosis=random.choice(diagnoses_list),
                    symptoms='Various symptoms reported',
                    treatment='Prescribed medication and lifestyle changes',
                    prescription='Medication as directed',
                    notes=f'Follow-up in {random.randint(1, 4)} weeks',
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
                )
                db.session.add(note)
                note_count += 1
        
        db.session.commit()
        print(f"✅ Generated {note_count} medical notes with diagnoses")
        
        print("=" * 40)
        print("✅ Sample data generation complete!")
        print(f"   - {vital_count} vital signs records")
        print(f"   - {note_count} medical notes with diagnoses")

if __name__ == '__main__':
    generate_sample_data()







