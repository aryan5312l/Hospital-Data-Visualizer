"""
Script to populate VitalSigns and MedicalNote data from patient CSV
This will enable patient trends and disease distribution charts
"""
import sys
import os
import csv
import random
from datetime import datetime, timedelta, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Patient, VitalSigns, MedicalNote, Doctor

def _approx_dob_from_age(age_years: int) -> date:
    return (date.today() - timedelta(days=age_years * 365))

with app.app_context():
    print("Loading patients from CSV...")
    
    # Read patient data from CSV
    patients_csv_data = {}
    with open('dummy_patients.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('name', '').strip()
            if not name:
                continue
            patients_csv_data[name] = {
                'age': int(row.get('age', '0') or 0),
                'diagnosis': row.get('diagnosis', ''),
                'severity': row.get('severity', 'Moderate'),
                'admission_date': row.get('admission_date', ''),
                'department': row.get('department', '')
            }
    
    print(f"Found {len(patients_csv_data)} patients in CSV")
    
    # Get all patients from database
    db_patients = Patient.query.all()
    print(f"Found {len(db_patients)} patients in database")
    
    # Create MedicalNote records from CSV diagnosis data
    print("\nCreating MedicalNote records...")
    medical_notes_created = 0
    
    for patient in db_patients:
        full_name = f"{patient.first_name} {patient.last_name}"
        csv_data = patients_csv_data.get(full_name)
        
        if not csv_data:
            continue
        
        # Check if medical note already exists
        existing_note = MedicalNote.query.filter_by(
            patient_id=patient.id,
            diagnosis=csv_data['diagnosis']
        ).first()
        
        if existing_note:
            continue
        
        # Find a doctor for this patient (use assigned doctor or any doctor)
        doctor = patient.assigned_doctor
        if not doctor:
            doctor = Doctor.query.first()
        
        if not doctor:
            continue
        
        # Parse admission date
        admission_date = None
        if csv_data['admission_date']:
            try:
                admission_date = datetime.strptime(csv_data['admission_date'], '%Y-%m-%d')
            except:
                admission_date = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        else:
            admission_date = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        
        # Create medical note
        medical_note = MedicalNote(
            patient_id=patient.id,
            doctor_id=doctor.id,
            diagnosis=csv_data['diagnosis'],
            symptoms=f"Patient reported symptoms related to {csv_data['diagnosis']}",
            treatment=f"Treatment plan for {csv_data['diagnosis']}",
            prescription="As prescribed by physician",
            notes=f"Severity: {csv_data['severity']}",
            created_at=admission_date
        )
        db.session.add(medical_note)
        medical_notes_created += 1
    
    db.session.commit()
    print(f"Created {medical_notes_created} medical notes")
    
    # Create VitalSigns records for each patient
    print("\nCreating VitalSigns records...")
    vitals_created = 0
    
    for patient in db_patients:
        full_name = f"{patient.first_name} {patient.last_name}"
        csv_data = patients_csv_data.get(full_name)
        
        # Check if patient already has vital signs
        existing_vitals = VitalSigns.query.filter_by(patient_id=patient.id).first()
        if existing_vitals:
            continue
        
        # Calculate age from DOB
        age = (date.today() - patient.date_of_birth).days // 365
        
        # Get diagnosis and severity from CSV
        diagnosis = csv_data.get('diagnosis', '') if csv_data else ''
        severity = csv_data.get('severity', 'Moderate') if csv_data else 'Moderate'
        
        # Parse admission date for base date
        base_date = patient.admission_date if patient.admission_date else patient.user.created_at.date()
        if isinstance(base_date, date):
            base_datetime = datetime.combine(base_date, datetime.min.time())
        else:
            base_datetime = datetime.utcnow() - timedelta(days=random.randint(30, 90))
        
        # Create 5-10 vital signs records per patient over time
        num_records = random.randint(5, 10)
        for i in range(num_records):
            record_date = base_datetime + timedelta(days=random.randint(0, 45))
            
            # Calculate vital signs based on age and severity
            age_factor = age / 100
            severity_factor = {'Mild': 1.0, 'Moderate': 1.2, 'Severe': 1.5}.get(severity, 1.2)
            
            heart_rate = int(60 + (20 * age_factor) + random.randint(-10, 10) * severity_factor)
            systolic_bp = int(110 + (10 * age_factor) + random.randint(-15, 15) * severity_factor)
            diastolic_bp = int(70 + (5 * age_factor) + random.randint(-10, 10) * severity_factor)
            temperature = round(36.5 + random.uniform(-0.5, 1.5), 1)
            weight = round(55 + random.uniform(-15, 25) + (age_factor * 10), 1)
            height = round(150 + random.uniform(-20, 30), 1)
            glucose = round(80 + random.uniform(-30, 50) + (30 if 'Diabetes' in diagnosis else 0), 1)
            
            vital = VitalSigns(
                patient_id=patient.id,
                heart_rate=max(50, min(120, heart_rate)),  # Clamp to reasonable range
                blood_pressure_systolic=max(90, min(180, systolic_bp)),
                blood_pressure_diastolic=max(60, min(120, diastolic_bp)),
                temperature=max(35.0, min(39.0, temperature)),
                weight=max(30, min(150, weight)),
                height=max(100, min(220, height)),
                glucose_level=glucose if glucose > 0 else None,
                recorded_at=record_date
            )
            db.session.add(vital)
            vitals_created += 1
        
        # Commit in batches
        if vitals_created % 100 == 0:
            db.session.commit()
    
    db.session.commit()
    
    print(f"\n✅ Data population complete!")
    print(f"   Medical Notes created: {medical_notes_created}")
    print(f"   Vital Signs records created: {vitals_created}")
    
    # Verify
    total_vitals = VitalSigns.query.count()
    total_notes = MedicalNote.query.count()
    print(f"\n   Total Vital Signs in DB: {total_vitals}")
    print(f"   Total Medical Notes in DB: {total_notes}")
    print("\n✅ Charts should now display data!")


