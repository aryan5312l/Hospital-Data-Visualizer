"""
Sample Data Generator for Hospital Management System
This script generates comprehensive dummy data for testing and demonstration
"""

import random
from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_dummy_data(
    num_patients: int = 1200,
    vitals_per_patient=(10, 15),
    labs_per_patient=(3, 5),
    department_days: int = 120
):
    """Generate comprehensive dummy data for the hospital system.

    Each exported dataset (patients, vital signs, lab reports, department stats)
    is guaranteed to contain at least 1,000 rows by default.
    """
    
    random.seed()
    np.random.seed()
    
    departments = [
        'Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 
        'Oncology', 'Dermatology', 'Gastroenterology', 'Endocrinology', 'Psychiatry'
    ]
    
    department_diagnoses = {
        'Cardiology': ['Hypertension', 'Arrhythmia', 'Heart Disease', 'Angina'],
        'Neurology': ['Migraine', 'Epilepsy', 'Stroke', 'Headache'],
        'Pediatrics': ['Common Cold', 'Fever', 'Allergies', 'Bronchitis'],
        'Orthopedics': ['Fracture', 'Arthritis', 'Back Pain', 'Knee Injury'],
        'Oncology': ['Cancer', 'Cancer Screening', 'Chemotherapy'],
        'Dermatology': ['Skin Allergy', 'Eczema', 'Psoriasis', 'Dermatitis'],
        'Gastroenterology': ['Ulcer', 'Gastritis', 'Acid Reflux', 'Digestive Issues'],
        'Endocrinology': ['Diabetes', 'Thyroid Disorder', 'Hormone Imbalance'],
        'Psychiatry': ['Anxiety', 'Depression', 'Stress', 'Bipolar Disorder']
    }
    
    severity_levels = ['Mild', 'Moderate', 'Severe']
    severity_weights = [0.45, 0.4, 0.15]
    
    first_names = [
        'Aarav', 'Diya', 'Isha', 'Rohit', 'Sneha', 'Vikram', 'Meera', 'Ananya', 'Rajesh',
        'Kavya', 'Arjun', 'Pooja', 'Suresh', 'Nikhil', 'Radha', 'Aditya', 'Neha', 'Sunita',
        'Kiran', 'Deepika', 'Pranav', 'Amit', 'Swati', 'Manish', 'Anjali', 'Vedant',
        'Shreya', 'Ramesh', 'Priya', 'Siddharth'
    ]
    last_names = [
        'Sharma', 'Verma', 'Patel', 'Iyer', 'Gupta', 'Rao', 'Kapoor', 'Nair', 'Singh',
        'Desai', 'Mehta', 'Kumar', 'Shah', 'Malhotra', 'Agarwal', 'Reddy', 'Joshi', 'Kapoor',
        'Nair', 'Iyengar', 'Bose', 'Lal', 'Menon', 'Khanna', 'Bajaj', 'Chopra', 'Dutta'
    ]
    
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    genders = ['Male', 'Female', 'Other']
    
    def random_name():
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def random_admission_date():
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        delta_days = (end - start).days
        return (start + timedelta(days=random.randint(0, delta_days))).strftime('%Y-%m-%d')
    
    def pick_severity():
        return random.choices(severity_levels, weights=severity_weights, k=1)[0]
    
    patients_data = []
    for pid in range(1, num_patients + 1):
        dept = random.choice(departments)
        diagnosis = random.choice(department_diagnoses[dept])
        severity = pick_severity()
        age = random.randint(1, 90)
        patient = {
            'id': pid,
            'name': random_name(),
            'age': age,
            'gender': random.choice(genders),
            'blood_group': random.choice(blood_groups),
            'department': dept,
            'admission_date': random_admission_date(),
            'diagnosis': diagnosis,
            'severity': severity
        }
        patients_data.append(patient)
    
    # Generate vital signs data for each patient over time
    vital_signs_data = []
    vitals_min, vitals_max = vitals_per_patient
    for patient in patients_data:
        base_date = datetime.strptime(patient['admission_date'], '%Y-%m-%d')
        for _ in range(random.randint(vitals_min, vitals_max)):
            record_date = base_date + timedelta(days=random.randint(0, 45))
            age_factor = patient['age'] / 100
            severity_factor = {'Mild': 1.0, 'Moderate': 1.2, 'Severe': 1.5}[patient['severity']]
            heart_rate = int(60 + (20 * age_factor) + random.randint(-10, 10) * severity_factor)
            systolic_bp = int(110 + (10 * age_factor) + random.randint(-15, 15) * severity_factor)
            diastolic_bp = int(70 + (5 * age_factor) + random.randint(-10, 10) * severity_factor)
            temperature = round(36.5 + random.uniform(-0.5, 1.5), 1)
            weight = round(55 + random.uniform(-15, 25) + (age_factor * 10), 1)
            height = round(150 + random.uniform(-20, 30), 1)
            glucose = round(80 + random.uniform(-30, 50) + (30 if 'Diabetes' in patient['diagnosis'] else 0), 1)
            
            vital_signs_data.append({
                'patient_id': patient['id'],
                'patient_name': patient['name'],
                'record_date': record_date.strftime('%Y-%m-%d'),
                'heart_rate': heart_rate,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'temperature': temperature,
                'weight': weight,
                'height': height,
                'glucose': glucose,
                'bmi': round(weight / ((height/100) ** 2), 1)
            })
    
    # Generate lab test data
    lab_tests = [
        'Blood Glucose', 'Cholesterol', 'Hemoglobin', 'White Blood Cells',
        'Red Blood Cells', 'Platelets', 'Creatinine', 'Urea', 'Sodium',
        'Potassium', 'Calcium', 'Iron', 'Vitamin D', 'Thyroid Stimulating Hormone'
    ]
    
    lab_reports_data = []
    labs_min, labs_max = labs_per_patient
    for patient in patients_data:
        admission_dt = datetime.strptime(patient['admission_date'], '%Y-%m-%d')
        for _ in range(random.randint(labs_min, labs_max)):
            test_date = admission_dt + timedelta(days=random.randint(1, 30))
            test_name = random.choice(lab_tests)
            if test_name == 'Blood Glucose':
                normal_range = '70-100'
                base = 80
                delta = random.uniform(-20, 40)
                condition_adjustment = 30 if 'Diabetes' in patient['diagnosis'] else 0
                result = round(base + delta + condition_adjustment, 1)
            elif test_name == 'Cholesterol':
                normal_range = '0-200'
                result = round(150 + random.uniform(-30, 50), 1)
            elif test_name == 'Hemoglobin':
                normal_range = '12-16'
                result = round(13 + random.uniform(-2, 2), 1)
            else:
                normal_range = '10-100'
                result = round(50 + random.uniform(-20, 30), 1)
            status = 'normal' if result <= 100 else 'abnormal' if result <= 150 else 'critical'
            lab_reports_data.append({
                'patient_id': patient['id'],
                'patient_name': patient['name'],
                'test_name': test_name,
                'test_date': test_date.strftime('%Y-%m-%d'),
                'result': result,
                'normal_range': normal_range,
                'status': status
            })
    
    # Generate department statistics with >= 1,000 rows
    department_stats = []
    stats_start = datetime(2024, 1, 1)
    for day in range(department_days):
        report_date = (stats_start + timedelta(days=day)).strftime('%Y-%m-%d')
        for dept in departments:
            dept_patients = [p for p in patients_data if p['department'] == dept]
            if not dept_patients:
                continue
            sample_size = random.randint(5, min(50, len(dept_patients)))
            sampled_patients = random.sample(dept_patients, sample_size)
            severity_counts = Counter(p['severity'] for p in sampled_patients)
            department_stats.append({
                'report_date': report_date,
                'department': dept,
                'patient_count': sample_size,
                'avg_age': round(sum(p['age'] for p in sampled_patients) / sample_size, 1),
                'severity_distribution': {
                    level: severity_counts.get(level, 0) for level in severity_levels
                }
            })
    
    assert len(patients_data) >= 1000, "Patients dataset must have at least 1,000 rows."
    assert len(vital_signs_data) >= 1000, "Vital signs dataset must have at least 1,000 rows."
    assert len(lab_reports_data) >= 1000, "Lab reports dataset must have at least 1,000 rows."
    assert len(department_stats) >= 1000, "Department stats dataset must have at least 1,000 rows."
    
    return {
        'patients': patients_data,
        'vital_signs': vital_signs_data,
        'lab_reports': lab_reports_data,
        'departments': department_stats
    }

def save_data_to_csv():
    """Save generated data to CSV files for analysis"""
    data = generate_dummy_data()
    
    # Save patients data
    patients_df = pd.DataFrame(data['patients'])
    patients_df.to_csv('dummy_patients.csv', index=False)
    
    # Save vital signs data
    vitals_df = pd.DataFrame(data['vital_signs'])
    vitals_df.to_csv('dummy_vital_signs.csv', index=False)
    
    # Save lab reports data
    lab_df = pd.DataFrame(data['lab_reports'])
    lab_df.to_csv('dummy_lab_reports.csv', index=False)
    
    # Save department statistics
    dept_df = pd.DataFrame(data['departments'])
    dept_df.to_csv('dummy_departments.csv', index=False)
    
    print("✅ Dummy data saved to CSV files:")
    print("   - dummy_patients.csv")
    print("   - dummy_vital_signs.csv") 
    print("   - dummy_lab_reports.csv")
    print("   - dummy_departments.csv")

if __name__ == '__main__':
    save_data_to_csv()
