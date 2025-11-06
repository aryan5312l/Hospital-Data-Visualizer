from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.utils
import json
import os
from functools import wraps
import random
from datetime import date, timedelta
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Public endpoints (no auth)
@app.route('/api/public/doctors', methods=['GET'])
def public_doctors():
    doctors = Doctor.query.all()
    return jsonify([
        {
            'id': d.id,
            'name': f"{d.first_name} {d.last_name}",
            'specialization': d.specialization,
            'department': d.department
        } for d in doctors
    ])

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, patient, lab_tech
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)
    lab_tech_profile = db.relationship('LabTechnician', backref='user', uselist=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    patients = db.relationship('Patient', backref='assigned_doctor')
    appointments = db.relationship('Appointment', backref='doctor')
    medical_notes = db.relationship('MedicalNote', backref='doctor')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=False)
    medical_history = db.Column(db.Text)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient')
    medical_notes = db.relationship('MedicalNote', backref='patient')
    lab_reports = db.relationship('LabReport', backref='patient')
    vitals = db.relationship('VitalSigns', backref='patient')

class LabTechnician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    certification = db.Column(db.String(100), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MedicalNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    symptoms = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LabReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    result_value = db.Column(db.Float, nullable=False)
    normal_range = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='normal')  # normal, abnormal, critical
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VitalSigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure_systolic = db.Column(db.Integer, nullable=False)
    blood_pressure_diastolic = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    glucose_level = db.Column(db.Float, nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

# Role-based access control decorator
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                if not current_user_id:
                    return jsonify({'message': 'No token provided'}), 401
                
                user = User.query.get(int(current_user_id))
                if not user:
                    return jsonify({'message': 'User not found'}), 404
                
                if user.role not in roles:
                    return jsonify({'message': 'Access denied'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'message': f'Authentication error: {str(e)}'}), 401
        return decorated_function
    return decorator

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        role=data['role']
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Create role-specific profile
    if data['role'] == 'doctor':
        doctor = Doctor(
            user_id=user.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialization=data['specialization'],
            department=data['department'],
            phone=data['phone'],
            license_number=data['license_number']
        )
        db.session.add(doctor)
    elif data['role'] == 'patient':
        patient = Patient(
            user_id=user.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            gender=data['gender'],
            phone=data['phone'],
            address=data['address'],
            emergency_contact=data['emergency_contact']
        )
        db.session.add(patient)
    elif data['role'] == 'lab_tech':
        lab_tech = LabTechnician(
            user_id=user.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data['department'],
            phone=data['phone'],
            certification=data['certification']
        )
        db.session.add(lab_tech)
    
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Dashboard routes
@app.route('/api/dashboard/admin', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def admin_dashboard():
    # Get statistics
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    total_lab_reports = LabReport.query.count()
    
    # Get recent appointments
    recent_appointments = db.session.query(Appointment, Patient, Doctor).join(
        Patient, Appointment.patient_id == Patient.id
    ).join(
        Doctor, Appointment.doctor_id == Doctor.id
    ).order_by(Appointment.appointment_date.desc()).limit(10).all()
    
    appointments_data = []
    for appointment, patient, doctor in recent_appointments:
        appointments_data.append({
            'id': appointment.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            'doctor_name': f"{doctor.first_name} {doctor.last_name}",
            'date': appointment.appointment_date.isoformat(),
            'status': appointment.status
        })
    
    return jsonify({
        'statistics': {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'total_lab_reports': total_lab_reports
        },
        'recent_appointments': appointments_data
    })

@app.route('/api/dashboard/doctor', methods=['GET'])
@jwt_required()
@role_required(['doctor'])
def doctor_dashboard():
    current_user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=current_user_id).first()
    
    if not doctor:
        return jsonify({'message': 'Doctor profile not found'}), 404
    
    # Get doctor's patients
    patients = Patient.query.filter_by(doctor_id=doctor.id).all()
    patient_data = []
    
    for patient in patients:
        # Get latest vital signs
        latest_vitals = VitalSigns.query.filter_by(patient_id=patient.id).order_by(
            VitalSigns.recorded_at.desc()
        ).first()
        
        # Get latest lab reports
        latest_lab = LabReport.query.filter_by(patient_id=patient.id).order_by(
            LabReport.created_at.desc()
        ).first()
        
        patient_data.append({
            'id': patient.id,
            'name': f"{patient.first_name} {patient.last_name}",
            'age': (date.today() - patient.date_of_birth).days // 365,
            'gender': patient.gender,
            'latest_vitals': {
                'heart_rate': latest_vitals.heart_rate if latest_vitals else None,
                'blood_pressure': f"{latest_vitals.blood_pressure_systolic}/{latest_vitals.blood_pressure_diastolic}" if latest_vitals else None,
                'temperature': latest_vitals.temperature if latest_vitals else None
            } if latest_vitals else None,
            'latest_lab': {
                'test_name': latest_lab.test_name if latest_lab else None,
                'result': latest_lab.result_value if latest_lab else None,
                'status': latest_lab.status if latest_lab else None
            } if latest_lab else None
        })
    
    return jsonify({
        'doctor': {
            'name': f"{doctor.first_name} {doctor.last_name}",
            'specialization': doctor.specialization,
            'department': doctor.department
        },
        'patients': patient_data
    })

@app.route('/api/dashboard/patient', methods=['GET'])
@jwt_required()
@role_required(['patient'])
def patient_dashboard():
    current_user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    
    if not patient:
        return jsonify({'message': 'Patient profile not found'}), 404
    
    # Get patient's medical history
    medical_notes = MedicalNote.query.filter_by(patient_id=patient.id).order_by(
        MedicalNote.created_at.desc()
    ).limit(5).all()
    
    # Get lab reports
    lab_reports = LabReport.query.filter_by(patient_id=patient.id).order_by(
        LabReport.created_at.desc()
    ).limit(5).all()
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status='scheduled'
    ).filter(Appointment.appointment_date > datetime.utcnow()).order_by(
        Appointment.appointment_date
    ).limit(5).all()
    
    return jsonify({
        'patient': {
            'name': f"{patient.first_name} {patient.last_name}",
            'age': (date.today() - patient.date_of_birth).days // 365,
            'gender': patient.gender
        },
        'medical_notes': [{
            'diagnosis': note.diagnosis,
            'treatment': note.treatment,
            'date': note.created_at.isoformat()
        } for note in medical_notes],
        'lab_reports': [{
            'test_name': report.test_name,
            'result': report.result_value,
            'status': report.status,
            'date': report.created_at.isoformat()
        } for report in lab_reports],
        'upcoming_appointments': [{
            'date': appointment.appointment_date.isoformat(),
            'doctor': f"{appointment.doctor.first_name} {appointment.doctor.last_name}",
            'status': appointment.status
        } for appointment in upcoming_appointments]
    })

# Data visualization routes
@app.route('/api/analytics/patient-trends', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor'])
def patient_trends():
    # Get patient vital signs over time
    vitals_data = db.session.query(VitalSigns, Patient).join(
        Patient, VitalSigns.patient_id == Patient.id
    ).order_by(VitalSigns.recorded_at).all()
    
    if not vitals_data:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title='Patient Health Trends Over Time',
            xaxis_title='Date',
            yaxis_title='Values',
            annotations=[dict(text='No data available', x=0.5, y=0.5, showarrow=False)]
        )
        return jsonify({
            'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
        })
    
    # Create DataFrame for analysis
    df = pd.DataFrame([{
        'date': vital.recorded_at,
        'patient_id': vital.patient_id,
        'patient_name': f"{patient.first_name} {patient.last_name}",
        'heart_rate': vital.heart_rate,
        'systolic_bp': vital.blood_pressure_systolic,
        'diastolic_bp': vital.blood_pressure_diastolic,
        'temperature': vital.temperature,
        'glucose': vital.glucose_level
    } for vital, patient in vitals_data])
    
    # Create Plotly visualization
    fig = go.Figure()
    
    # Add heart rate trend
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['heart_rate'],
        mode='lines+markers',
        name='Heart Rate',
        line=dict(color='red')
    ))
    
    # Add blood pressure trend
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['systolic_bp'],
        mode='lines+markers',
        name='Systolic BP',
        line=dict(color='blue')
    ))
    
    # Add glucose trend
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['glucose'],
        mode='lines+markers',
        name='Glucose Level',
        line=dict(color='green')
    ))
    
    fig.update_layout(
        title='Patient Health Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Values',
        hovermode='x unified'
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

@app.route('/api/analytics/disease-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor'])
def disease_distribution():
    # Get diagnosis data
    diagnoses = db.session.query(MedicalNote.diagnosis).all()
    
    if not diagnoses:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title='Disease Distribution',
            annotations=[dict(text='No data available', x=0.5, y=0.5, showarrow=False)]
        )
        return jsonify({
            'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
        })
    
    # Count diagnoses
    diagnosis_counts = {}
    for (diagnosis,) in diagnoses:
        diagnosis_counts[diagnosis] = diagnosis_counts.get(diagnosis, 0) + 1
    
    # Create Plotly pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(diagnosis_counts.keys()),
        values=list(diagnosis_counts.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title='Disease Distribution',
        annotations=[dict(text='Diseases', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

@app.route('/api/analytics/department-performance', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def department_performance():
    # Get department data
    departments = db.session.query(Doctor.department, db.func.count(Patient.id)).join(
        Patient, Doctor.id == Patient.doctor_id
    ).group_by(Doctor.department).all()
    
    if not departments:
        return jsonify({'message': 'No data available'}), 404
    
    # Create Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=[dept[0] for dept in departments],
            y=[dept[1] for dept in departments],
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title='Patient Distribution by Department',
        xaxis_title='Department',
        yaxis_title='Number of Patients'
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

@app.route('/api/analytics/age-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor'])
def age_distribution():
    # Get patient age data
    patients = Patient.query.all()
    
    if not patients:
        return jsonify({'message': 'No data available'}), 404
    
    # Calculate ages
    ages = []
    for patient in patients:
        age = (date.today() - patient.date_of_birth).days // 365
        ages.append(age)
    
    # Create age groups
    age_groups = {'0-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0}
    for age in ages:
        if age <= 18:
            age_groups['0-18'] += 1
        elif age <= 35:
            age_groups['19-35'] += 1
        elif age <= 50:
            age_groups['36-50'] += 1
        elif age <= 65:
            age_groups['51-65'] += 1
        else:
            age_groups['65+'] += 1
    
    # Create Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(age_groups.keys()),
            y=list(age_groups.values()),
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
    ])
    
    fig.update_layout(
        title='Patient Age Distribution',
        xaxis_title='Age Groups',
        yaxis_title='Number of Patients',
        showlegend=False
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

@app.route('/api/analytics/lab-results-analysis', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor', 'lab_tech'])
def lab_results_analysis():
    # Get lab reports data
    lab_reports = LabReport.query.all()
    
    if not lab_reports:
        # Return empty chart with annotation so UI still renders
        fig = go.Figure()
        fig.update_layout(
            title='Lab Test Results Analysis',
            annotations=[dict(text='No lab data available', x=0.5, y=0.5, showarrow=False)]
        )
        return jsonify({'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig)), 'summary': {'total_tests': 0, 'normal_results': 0, 'abnormal_results': 0, 'critical_results': 0}})
    
    # Analyze lab results
    test_types = {}
    status_counts = {'normal': 0, 'abnormal': 0, 'critical': 0}
    
    for report in lab_reports:
        test_name = report.test_name
        if test_name not in test_types:
            test_types[test_name] = {'normal': 0, 'abnormal': 0, 'critical': 0}
        
        test_types[test_name][report.status] += 1
        status_counts[report.status] += 1
    
    # Create stacked bar chart for test results
    fig = go.Figure()
    
    test_names = list(test_types.keys())
    normal_counts = [test_types[name]['normal'] for name in test_names]
    abnormal_counts = [test_types[name]['abnormal'] for name in test_names]
    critical_counts = [test_types[name]['critical'] for name in test_names]
    
    fig.add_trace(go.Bar(name='Normal', x=test_names, y=normal_counts, marker_color='#2ECC71'))
    fig.add_trace(go.Bar(name='Abnormal', x=test_names, y=abnormal_counts, marker_color='#F39C12'))
    fig.add_trace(go.Bar(name='Critical', x=test_names, y=critical_counts, marker_color='#E74C3C'))
    
    fig.update_layout(
        title='Lab Test Results Analysis',
        xaxis_title='Test Types',
        yaxis_title='Number of Results',
        barmode='stack'
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig)),
        'summary': {
            'total_tests': len(lab_reports),
            'normal_results': status_counts['normal'],
            'abnormal_results': status_counts['abnormal'],
            'critical_results': status_counts['critical']
        }
    })

@app.route('/api/analytics/monthly-admissions', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def monthly_admissions():
    # Get patient admission data (using created_at as proxy for admission)
    patients = Patient.query.all()
    
    if not patients:
        return jsonify({'message': 'No data available'}), 404
    
    # Group by month
    monthly_data = {}
    for patient in patients:
        month_key = patient.user.created_at.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = 0
        monthly_data[month_key] += 1
    
    # Sort by month
    sorted_months = sorted(monthly_data.keys())
    admission_counts = [monthly_data[month] for month in sorted_months]
    
    # Create line chart
    fig = go.Figure(data=[
        go.Scatter(
            x=sorted_months,
            y=admission_counts,
            mode='lines+markers',
            line=dict(color='#3498DB', width=3),
            marker=dict(size=8)
        )
    ])
    
    fig.update_layout(
        title='Monthly Patient Admissions',
        xaxis_title='Month',
        yaxis_title='Number of Admissions',
        hovermode='x unified'
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

@app.route('/api/analytics/gender-analysis', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor'])
def gender_analysis():
    # Get patient gender data
    patients = Patient.query.all()
    
    if not patients:
        return jsonify({'message': 'No data available'}), 404
    
    # Count by gender
    gender_counts = {'Male': 0, 'Female': 0}
    for patient in patients:
        gender_counts[patient.gender] += 1
    
    # Create pie chart
    fig = go.Figure(data=[
        go.Pie(
            labels=list(gender_counts.keys()),
            values=list(gender_counts.values()),
            hole=0.3,
            marker_colors=['#3498DB', '#E91E63']
        )
    ])
    
    fig.update_layout(
        title='Patient Gender Distribution',
        annotations=[dict(text='Gender', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return jsonify({
        'chart': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    })

# CRUD operations for patients
@app.route('/api/patients', methods=['GET'])
@jwt_required()
@role_required(['admin', 'doctor'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'name': f"{p.first_name} {p.last_name}",
        'age': (date.today() - p.date_of_birth).days // 365,
        'gender': p.gender,
        'phone': p.phone,
        'doctor': f"{p.assigned_doctor.first_name} {p.assigned_doctor.last_name}" if p.assigned_doctor else None
    } for p in patients])

@app.route('/api/patients/<int:patient_id>/vitals', methods=['POST'])
@jwt_required()
@role_required(['doctor', 'lab_tech'])
def add_vital_signs(patient_id):
    data = request.get_json()
    
    vital = VitalSigns(
        patient_id=patient_id,
        heart_rate=data['heart_rate'],
        blood_pressure_systolic=data['blood_pressure_systolic'],
        blood_pressure_diastolic=data['blood_pressure_diastolic'],
        temperature=data['temperature'],
        weight=data['weight'],
        height=data['height'],
        glucose_level=data.get('glucose_level')
    )
    
    db.session.add(vital)
    db.session.commit()
    
    return jsonify({'message': 'Vital signs recorded successfully'}), 201

@app.route('/api/patients/<int:patient_id>/lab-reports', methods=['POST'])
@jwt_required()
@role_required(['lab_tech'])
def add_lab_report(patient_id):
    data = request.get_json()
    
    report = LabReport(
        patient_id=patient_id,
        test_name=data['test_name'],
        test_type=data['test_type'],
        result_value=data['result_value'],
        normal_range=data['normal_range'],
        status=data.get('status', 'normal'),
        notes=data.get('notes')
    )
    
    db.session.add(report)
    db.session.commit()
    
    return jsonify({'message': 'Lab report added successfully'}), 201

# Admin-only: import patients from CSV into the database
def _generate_unique_username(base_username: str) -> str:
    candidate = base_username.lower().replace(' ', '_')
    if not User.query.filter_by(username=candidate).first():
        return candidate
    suffix = 1
    while True:
        cand = f"{candidate}{suffix}"
        if not User.query.filter_by(username=cand).first():
            return cand
        suffix += 1

def _approx_dob_from_age(age_years: int) -> date:
    # Approximate DOB as today minus age in years (365 days per year) to avoid month/day complexity
    return (date.today() - timedelta(days=age_years * 365))

def _find_doctor_for_department(department: str):
    if not department:
        return None
    doctor = Doctor.query.filter(db.func.lower(Doctor.department) == department.lower()).first()
    if doctor:
        return doctor
    return Doctor.query.first()

def import_patients_from_csv(csv_path: str) -> int:
    if not os.path.exists(csv_path):
        return 0
    imported = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            full_name = row.get('name', '').strip()
            if not full_name:
                continue
            first_name, last_name = (full_name.split(' ', 1) + [''])[:2]
            age = int(row.get('age', '0') or 0)
            gender = row.get('gender', 'Male')
            department = row.get('department', '')

            base_username = (first_name + (last_name[:1] if last_name else '')).lower() or 'patient'
            username = _generate_unique_username(base_username)
            email = f"{username}@example.com"

            if User.query.filter((User.username == username) | (User.email == email)).first():
                continue

            user = User(
                username=username,
                email=email,
                password_hash=bcrypt.generate_password_hash('patient123').decode('utf-8'),
                role='patient'
            )
            db.session.add(user)
            db.session.flush()

            doctor = _find_doctor_for_department(department)
            patient = Patient(
                user_id=user.id,
                doctor_id=doctor.id if doctor else None,
                first_name=first_name or 'Patient',
                last_name=last_name or 'User',
                date_of_birth=_approx_dob_from_age(age),
                gender=gender,
                phone=f"555-{random.randint(1000,9999)}",
                address=row.get('address') or 'N/A',
                emergency_contact=row.get('emergency_contact') or 'N/A'
            )
            db.session.add(patient)
            imported += 1

    db.session.commit()
    return imported

@app.route('/api/admin/import-patients', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def import_patients_endpoint():
    source = request.args.get('source', 'dummy_patients.csv')
    count = import_patients_from_csv(source)
    return jsonify({'imported': count, 'source': source}), 200

# Admin-only: import doctors from CSV into the database
def import_doctors_from_csv(csv_path: str) -> int:
    if not os.path.exists(csv_path):
        return 0
    imported = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            first_name = row.get('first_name', '').strip() or 'Doctor'
            last_name = row.get('last_name', '').strip() or 'User'
            username_base = (first_name + last_name[:1]).lower()
            username = _generate_unique_username(username_base)
            email = f"{username}@example.com"

            if User.query.filter((User.username == username) | (User.email == email)).first():
                continue

            user = User(
                username=username,
                email=email,
                password_hash=bcrypt.generate_password_hash('doctor123').decode('utf-8'),
                role='doctor'
            )
            db.session.add(user)
            db.session.flush()

            doctor = Doctor(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                specialization=row.get('specialization', 'General Medicine'),
                department=row.get('department', 'General'),
                phone=row.get('phone', f"555-{random.randint(1000,9999)}"),
                license_number=row.get('license_number', f"MD{random.randint(100000,999999)}")
            )
            db.session.add(doctor)
            imported += 1
    db.session.commit()
    return imported

@app.route('/api/admin/import-doctors', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def import_doctors_endpoint():
    source = request.args.get('source', 'dummy_doctors.csv')
    count = import_doctors_from_csv(source)
    return jsonify({'imported': count, 'source': source}), 200

def import_lab_reports_from_csv(csv_path: str) -> int:
    if not os.path.exists(csv_path):
        return 0
    # Build patient lookup by full name
    patients = {f"{p.first_name} {p.last_name}": p for p in Patient.query.all()}
    imported = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('patient_name') or row.get('name') or ''
            patient = patients.get(name)
            if not patient:
                # Try loose match on first token
                token = name.split(' ')[0] if name else ''
                patient = next((p for full, p in patients.items() if full.startswith(token)), None)
            if not patient:
                continue
            test_date_str = row.get('test_date') or row.get('date') or ''
            try:
                test_dt = datetime.fromisoformat(test_date_str)
            except Exception:
                try:
                    test_dt = datetime.strptime(test_date_str, '%Y-%m-%d')
                except Exception:
                    test_dt = datetime.utcnow()
            report = LabReport(
                patient_id=patient.id,
                test_name=row.get('test_name', 'Blood Test'),
                test_type=row.get('test_type', 'Diagnostic'),
                result_value=float(row.get('result') or row.get('result_value') or 0),
                normal_range=row.get('normal_range', '10-100'),
                status=row.get('status', 'normal'),
                notes=row.get('notes', ''),
                created_at=test_dt
            )
            db.session.add(report)
            imported += 1
    db.session.commit()
    return imported

def _delete_all_patient_data():
    # Delete dependent tables first
    LabReport.query.delete()
    VitalSigns.query.delete()
    MedicalNote.query.delete()
    Appointment.query.delete()
    # Delete patients and their user accounts
    patient_users = User.query.join(Patient, Patient.user_id == User.id).all()
    Patient.query.delete()
    for u in patient_users:
        db.session.delete(u)
    db.session.commit()

def _delete_all_doctors(keep_user_ids=None):
    keep_user_ids = set(keep_user_ids or [])
    # Unassign patients first
    for p in Patient.query.all():
        p.doctor_id = None
    db.session.flush()
    doctor_users = User.query.join(Doctor, Doctor.user_id == User.id).filter(~User.id.in_(keep_user_ids)).all()
    Doctor.query.filter(~Doctor.user_id.in_(keep_user_ids)).delete(synchronize_session=False)
    for u in doctor_users:
        db.session.delete(u)
    db.session.commit()

@app.route('/api/admin/reset-and-import', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def reset_and_import_endpoint():
    # Optional params: doctors, patients
    doctors_csv = request.args.get('doctors', 'dummy_doctors.csv')
    patients_csv = request.args.get('patients', 'dummy_patients.csv')
    labs_csv = request.args.get('labs', 'dummy_lab_reports.csv')

    # Keep admin user
    admin_users = [u.id for u in User.query.filter_by(role='admin').all()]

    # Wipe old data
    _delete_all_patient_data()
    _delete_all_doctors(keep_user_ids=admin_users)

    # Import doctors, then patients
    imported_doctors = import_doctors_from_csv(doctors_csv)
    imported_patients = import_patients_from_csv(patients_csv)
    imported_labs = import_lab_reports_from_csv(labs_csv)

    # Optionally add some vitals so charts are meaningful
    patients = Patient.query.all()
    for patient in patients:
        for i in range(6):
            vs = VitalSigns(
                patient_id=patient.id,
                heart_rate=random.randint(62, 98),
                blood_pressure_systolic=random.randint(108, 142),
                blood_pressure_diastolic=random.randint(68, 92),
                temperature=round(random.uniform(36.4, 37.6), 1),
                weight=round(random.uniform(50, 95), 1),
                height=round(random.uniform(150, 185), 1),
                glucose_level=round(random.uniform(75, 140), 1),
                recorded_at=datetime.utcnow() - timedelta(days=(6-i)*5)
            )
            db.session.add(vs)
    db.session.commit()

    return jsonify({
        'imported_doctors': imported_doctors,
        'imported_patients': imported_patients,
        'imported_lab_reports': imported_labs,
        'doctors_source': doctors_csv,
        'patients_source': patients_csv,
        'labs_source': labs_csv
    }), 200

# Assign a doctor to a patient
@app.route('/api/patients/<int:patient_id>/assign-doctor', methods=['POST'])
@jwt_required()
@role_required(['admin', 'doctor'])
def assign_doctor(patient_id: int):
    data = request.get_json() or {}
    doctor_id = data.get('doctor_id')
    if not doctor_id:
        return jsonify({'message': 'doctor_id is required'}), 400
    patient = Patient.query.get(patient_id)
    doctor = Doctor.query.get(doctor_id)
    if not patient or not doctor:
        return jsonify({'message': 'Patient or Doctor not found'}), 404
    patient.doctor_id = doctor.id
    db.session.commit()
    return jsonify({'message': 'Doctor assigned successfully'}), 200

@app.route('/api/patients/<int:patient_id>/medical-notes', methods=['POST'])
@jwt_required()
@role_required(['doctor'])
def add_medical_note(patient_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=current_user_id).first()
    
    if not doctor:
        return jsonify({'message': 'Doctor profile not found'}), 404
    
    note = MedicalNote(
        patient_id=patient_id,
        doctor_id=doctor.id,
        diagnosis=data['diagnosis'],
        symptoms=data.get('symptoms', ''),
        treatment=data.get('treatment', ''),
        prescription=data.get('prescription', ''),
        notes=data.get('notes', '')
    )
    
    db.session.add(note)
    db.session.commit()
    
    return jsonify({'message': 'Medical note added successfully'}), 201

# Initialize database and create sample data
def create_sample_data():
    # Create admin user
    admin_user = User(
        username='admin',
        email='admin@hospital.com',
        password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.commit()
    
    # Create sample doctors
    doctors_data = [
        {
            'username': 'dr_smith',
            'email': 'dr.smith@hospital.com',
            'password': 'doctor123',
            'first_name': 'John',
            'last_name': 'Smith',
            'specialization': 'Cardiology',
            'department': 'Cardiology',
            'phone': '555-0101',
            'license_number': 'MD123456'
        },
        {
            'username': 'dr_jones',
            'email': 'dr.jones@hospital.com',
            'password': 'doctor123',
            'first_name': 'Sarah',
            'last_name': 'Jones',
            'specialization': 'Neurology',
            'department': 'Neurology',
            'phone': '555-0102',
            'license_number': 'MD123457'
        }
    ]
    
    for doc_data in doctors_data:
        user = User(
            username=doc_data['username'],
            email=doc_data['email'],
            password_hash=bcrypt.generate_password_hash(doc_data['password']).decode('utf-8'),
            role='doctor'
        )
        db.session.add(user)
        db.session.commit()
        
        doctor = Doctor(
            user_id=user.id,
            first_name=doc_data['first_name'],
            last_name=doc_data['last_name'],
            specialization=doc_data['specialization'],
            department=doc_data['department'],
            phone=doc_data['phone'],
            license_number=doc_data['license_number']
        )
        db.session.add(doctor)
        db.session.commit()
    
    # Create sample patients
    patients_data = [
        {
            'username': 'patient1',
            'email': 'patient1@email.com',
            'password': 'patient123',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'date_of_birth': '1985-03-15',
            'gender': 'Female',
            'phone': '555-0201',
            'address': '123 Main St',
            'emergency_contact': 'Bob Johnson - 555-0202'
        },
        {
            'username': 'patient2',
            'email': 'patient2@email.com',
            'password': 'patient123',
            'first_name': 'Bob',
            'last_name': 'Williams',
            'date_of_birth': '1978-07-22',
            'gender': 'Male',
            'phone': '555-0203',
            'address': '456 Oak Ave',
            'emergency_contact': 'Jane Williams - 555-0204'
        }
    ]
    
    doctors = Doctor.query.all()
    for i, pat_data in enumerate(patients_data):
        user = User(
            username=pat_data['username'],
            email=pat_data['email'],
            password_hash=bcrypt.generate_password_hash(pat_data['password']).decode('utf-8'),
            role='patient'
        )
        db.session.add(user)
        db.session.commit()
        
        patient = Patient(
            user_id=user.id,
            doctor_id=doctors[i % len(doctors)].id,
            first_name=pat_data['first_name'],
            last_name=pat_data['last_name'],
            date_of_birth=datetime.strptime(pat_data['date_of_birth'], '%Y-%m-%d').date(),
            gender=pat_data['gender'],
            phone=pat_data['phone'],
            address=pat_data['address'],
            emergency_contact=pat_data['emergency_contact']
        )
        db.session.add(patient)
        db.session.commit()
    
    # Create sample vital signs
    patients = Patient.query.all()
    for patient in patients:
        for i in range(5):  # 5 records per patient
            vital = VitalSigns(
                patient_id=patient.id,
                heart_rate=random.randint(60, 100),
                blood_pressure_systolic=random.randint(110, 140),
                blood_pressure_diastolic=random.randint(70, 90),
                temperature=round(random.uniform(36.5, 37.5), 1),
                weight=round(random.uniform(60, 100), 1),
                height=round(random.uniform(150, 190), 1),
                glucose_level=round(random.uniform(80, 120), 1),
                recorded_at=datetime.utcnow() - timedelta(days=i*7)
            )
            db.session.add(vital)
    
    # Create sample medical notes
    diagnoses = ['Hypertension', 'Diabetes', 'Common Cold', 'Migraine', 'Arthritis']
    for patient in patients:
        for i in range(3):  # 3 notes per patient
            note = MedicalNote(
                patient_id=patient.id,
                doctor_id=patient.doctor_id,
                diagnosis=random.choice(diagnoses),
                symptoms='Various symptoms reported',
                treatment='Prescribed medication and lifestyle changes',
                prescription='Medication as directed',
                notes=f'Follow-up in {random.randint(1, 4)} weeks'
            )
            db.session.add(note)
    
    # Create sample lab reports
    test_types = ['Blood Test', 'Urine Test', 'X-Ray', 'MRI', 'CT Scan']
    for patient in patients:
        for i in range(2):  # 2 reports per patient
            report = LabReport(
                patient_id=patient.id,
                test_name=random.choice(test_types),
                test_type=random.choice(['Diagnostic', 'Screening', 'Monitoring']),
                result_value=round(random.uniform(10, 200), 2),
                normal_range='10-100',
                status=random.choice(['normal', 'abnormal']),
                notes='Results within normal range'
            )
            db.session.add(report)
    
    db.session.commit()

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard_page():
    return render_template('admin.html')

@app.route('/doctor')
def doctor_dashboard_page():
    return render_template('doctor.html')

@app.route('/patient')
def patient_dashboard_page():
    return render_template('patient.html')

@app.route('/lab')
def lab_dashboard_page():
    return render_template('lab.html')

@app.route('/signup')
def signup_page():
    return render_template('signup_patient.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            create_sample_data()
    app.run(debug=True)
