"""
Sample Data Generator for Hospital Management System
This script generates comprehensive dummy data for testing and demonstration
"""

import random
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

def generate_dummy_data():
    """Generate comprehensive dummy data for the hospital system"""
    
    # Sample patient data
    patients_data = [
        {
            'id': 1, 'name': 'Alice Johnson', 'age': 35, 'gender': 'Female',
            'department': 'Cardiology', 'admission_date': '2024-01-15',
            'diagnosis': 'Hypertension', 'severity': 'Moderate'
        },
        {
            'id': 2, 'name': 'Bob Williams', 'age': 42, 'gender': 'Male',
            'department': 'Neurology', 'admission_date': '2024-01-20',
            'diagnosis': 'Migraine', 'severity': 'Mild'
        },
        {
            'id': 3, 'name': 'Carol Davis', 'age': 28, 'gender': 'Female',
            'department': 'Pediatrics', 'admission_date': '2024-01-25',
            'diagnosis': 'Common Cold', 'severity': 'Mild'
        },
        {
            'id': 4, 'name': 'David Brown', 'age': 55, 'gender': 'Male',
            'department': 'Cardiology', 'admission_date': '2024-02-01',
            'diagnosis': 'Heart Disease', 'severity': 'Severe'
        },
        {
            'id': 5, 'name': 'Emma Wilson', 'age': 31, 'gender': 'Female',
            'department': 'Orthopedics', 'admission_date': '2024-02-05',
            'diagnosis': 'Fracture', 'severity': 'Moderate'
        },
        {
            'id': 6, 'name': 'Frank Miller', 'age': 67, 'gender': 'Male',
            'department': 'Oncology', 'admission_date': '2024-02-10',
            'diagnosis': 'Cancer', 'severity': 'Severe'
        },
        {
            'id': 7, 'name': 'Grace Lee', 'age': 24, 'gender': 'Female',
            'department': 'Dermatology', 'admission_date': '2024-02-15',
            'diagnosis': 'Skin Condition', 'severity': 'Mild'
        },
        {
            'id': 8, 'name': 'Henry Taylor', 'age': 49, 'gender': 'Male',
            'department': 'Gastroenterology', 'admission_date': '2024-02-20',
            'diagnosis': 'Digestive Issues', 'severity': 'Moderate'
        },
        {
            'id': 9, 'name': 'Ivy Chen', 'age': 33, 'gender': 'Female',
            'department': 'Endocrinology', 'admission_date': '2024-02-25',
            'diagnosis': 'Diabetes', 'severity': 'Moderate'
        },
        {
            'id': 10, 'name': 'Jack Anderson', 'age': 41, 'gender': 'Male',
            'department': 'Psychiatry', 'admission_date': '2024-03-01',
            'diagnosis': 'Anxiety', 'severity': 'Mild'
        }
    ]
    
    # Generate vital signs data for each patient over time
    vital_signs_data = []
    for patient in patients_data:
        base_date = datetime.strptime(patient['admission_date'], '%Y-%m-%d')
        
        # Generate 10-15 vital signs records per patient
        for i in range(random.randint(10, 15)):
            record_date = base_date + timedelta(days=random.randint(0, 30))
            
            # Generate realistic vital signs based on age and condition
            age_factor = patient['age'] / 100
            severity_factor = {'Mild': 1.0, 'Moderate': 1.2, 'Severe': 1.5}[patient['severity']]
            
            heart_rate = int(60 + (20 * age_factor) + random.randint(-10, 10) * severity_factor)
            systolic_bp = int(110 + (10 * age_factor) + random.randint(-15, 15) * severity_factor)
            diastolic_bp = int(70 + (5 * age_factor) + random.randint(-10, 10) * severity_factor)
            temperature = round(36.5 + random.uniform(-0.5, 1.5), 1)
            weight = round(60 + random.uniform(-10, 20) + (age_factor * 10), 1)
            height = round(150 + random.uniform(-20, 30), 1)
            glucose = round(80 + random.uniform(-20, 40) + (20 if patient['diagnosis'] == 'Diabetes' else 0), 1)
            
            vital_signs_data.append({
                'patient_id': patient['id'],
                'patient_name': patient['name'],
                'record_date': record_date,
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
    for patient in patients_data:
        # Generate 3-5 lab reports per patient
        for i in range(random.randint(3, 5)):
            test_date = datetime.strptime(patient['admission_date'], '%Y-%m-%d') + timedelta(days=random.randint(1, 20))
            test_name = random.choice(lab_tests)
            
            # Generate realistic test results
            if test_name == 'Blood Glucose':
                normal_range = '70-100'
                result = round(80 + random.uniform(-20, 40) + (30 if patient['diagnosis'] == 'Diabetes' else 0), 1)
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
                'test_date': test_date,
                'result': result,
                'normal_range': normal_range,
                'status': status
            })
    
    # Generate department statistics
    departments = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 
                  'Oncology', 'Dermatology', 'Gastroenterology', 'Endocrinology', 'Psychiatry']
    
    department_stats = []
    for dept in departments:
        dept_patients = [p for p in patients_data if p['department'] == dept]
        department_stats.append({
            'department': dept,
            'patient_count': len(dept_patients),
            'avg_age': round(sum(p['age'] for p in dept_patients) / len(dept_patients)) if dept_patients else 0,
            'severity_distribution': {
                'Mild': len([p for p in dept_patients if p['severity'] == 'Mild']),
                'Moderate': len([p for p in dept_patients if p['severity'] == 'Moderate']),
                'Severe': len([p for p in dept_patients if p['severity'] == 'Severe'])
            }
        })
    
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
