#!/usr/bin/env python3
"""
Fix Doctor and Patient Accounts Script
Ensures demo doctor and patient accounts exist with correct passwords
"""

from app import app, db, User, Doctor, Patient, bcrypt

def fix_accounts():
    """Ensure demo doctor and patient accounts exist"""
    print("🔧 Fixing Doctor and Patient Accounts...")
    print("=" * 40)
    
    with app.app_context():
        # Check and fix dr_smith
        doctor_user = User.query.filter_by(username='dr_smith', role='doctor').first()
        if not doctor_user:
            print("📝 Creating dr_smith account...")
            doctor_user = User(
                username='dr_smith',
                email='dr.smith@hospital.com',
                password_hash=bcrypt.generate_password_hash('doctor123').decode('utf-8'),
                role='doctor'
            )
            db.session.add(doctor_user)
            db.session.commit()
            
            # Create doctor profile
            doctor = Doctor(
                user_id=doctor_user.id,
                first_name='John',
                last_name='Smith',
                specialization='Cardiology',
                department='Cardiology',
                phone='555-0101',
                license_number='MD123456'
            )
            db.session.add(doctor)
            db.session.commit()
            print("✅ dr_smith account created")
        else:
            print("✅ dr_smith account exists")
            # Reset password to ensure it works
            doctor_user.password_hash = bcrypt.generate_password_hash('doctor123').decode('utf-8')
            db.session.commit()
            print("✅ dr_smith password reset")
        
        # Check and fix patient1
        patient_user = User.query.filter_by(username='patient1', role='patient').first()
        if not patient_user:
            print("📝 Creating patient1 account...")
            patient_user = User(
                username='patient1',
                email='patient1@email.com',
                password_hash=bcrypt.generate_password_hash('patient123').decode('utf-8'),
                role='patient'
            )
            db.session.add(patient_user)
            db.session.commit()
            
            # Get a doctor to assign
            doctor = Doctor.query.first()
            
            # Create patient profile
            patient = Patient(
                user_id=patient_user.id,
                doctor_id=doctor.id if doctor else None,
                first_name='Alice',
                last_name='Johnson',
                date_of_birth=datetime.strptime('1985-03-15', '%Y-%m-%d').date(),
                gender='Female',
                phone='555-0201',
                address='123 Main St',
                emergency_contact='Bob Johnson - 555-0202'
            )
            db.session.add(patient)
            db.session.commit()
            print("✅ patient1 account created")
        else:
            print("✅ patient1 account exists")
            # Reset password to ensure it works
            patient_user.password_hash = bcrypt.generate_password_hash('patient123').decode('utf-8')
            db.session.commit()
            print("✅ patient1 password reset")
        
        # Check and fix patient2
        patient_user2 = User.query.filter_by(username='patient2', role='patient').first()
        if not patient_user2:
            print("📝 Creating patient2 account...")
            patient_user2 = User(
                username='patient2',
                email='patient2@email.com',
                password_hash=bcrypt.generate_password_hash('patient123').decode('utf-8'),
                role='patient'
            )
            db.session.add(patient_user2)
            db.session.commit()
            
            # Get a doctor to assign
            doctor = Doctor.query.first()
            
            # Create patient profile
            patient2 = Patient(
                user_id=patient_user2.id,
                doctor_id=doctor.id if doctor else None,
                first_name='Bob',
                last_name='Williams',
                date_of_birth=datetime.strptime('1978-07-22', '%Y-%m-%d').date(),
                gender='Male',
                phone='555-0203',
                address='456 Oak Ave',
                emergency_contact='Jane Williams - 555-0204'
            )
            db.session.add(patient2)
            db.session.commit()
            print("✅ patient2 account created")
        else:
            print("✅ patient2 account exists")
            # Reset password to ensure it works
            patient_user2.password_hash = bcrypt.generate_password_hash('patient123').decode('utf-8')
            db.session.commit()
            print("✅ patient2 password reset")
        
        print("=" * 40)
        print("📋 Login Credentials:")
        print("   Doctor:  dr_smith / doctor123")
        print("   Patient: patient1 / patient123")
        print("   Patient: patient2 / patient123")
        print("=" * 40)
        print("✅ All accounts are ready to use!")

if __name__ == '__main__':
    from datetime import datetime
    fix_accounts()






