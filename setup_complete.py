#!/usr/bin/env python3
"""
Complete Setup Script for Hospital Management System
This script automates the entire setup process:
1. Generates CSV data files
2. Imports patients and doctors
3. Populates chart data (vital signs and medical notes)
4. Verifies all data is imported correctly
"""

import sys
import os
import subprocess

def run_command(command, description):
    """Run a command and display progress"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_file_exists(filename):
    """Check if a file exists"""
    return os.path.exists(filename)

def main():
    print("\n" + "="*60)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - COMPLETE SETUP")
    print("="*60)
    print("\nThis script will:")
    print("  1. Generate CSV data files (if needed)")
    print("  2. Import all patients and doctors")
    print("  3. Populate vital signs and medical notes for charts")
    print("  4. Verify all data is imported")
    print("\n" + "="*60)
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Step 1: Check/Generate CSV files
    print("\n📁 Step 1: Checking CSV files...")
    csv_files = ['dummy_patients.csv', 'dummy_doctors.csv', 'dummy_lab_reports.csv']
    missing_files = [f for f in csv_files if not check_file_exists(f)]
    
    if missing_files:
        print(f"⚠️  Missing files: {', '.join(missing_files)}")
        print("📊 Generating CSV files...")
        if not run_command("python sample_data.py", "Generating sample data CSV files"):
            print("❌ Failed to generate CSV files. Please run 'python sample_data.py' manually.")
            return
    else:
        print("✅ All CSV files exist")
    
    # Step 2: Initialize database
    print("\n💾 Step 2: Initializing database...")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app import app, db
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    # Step 3: Import patients
    print("\n👥 Step 3: Importing patients...")
    if not run_command("python reimport_all_patients.py", "Importing patients from CSV"):
        print("❌ Failed to import patients. Please check the error above.")
        return
    
    # Step 4: Populate chart data
    print("\n📊 Step 4: Populating chart data...")
    if not run_command("python populate_chart_data.py", "Creating vital signs and medical notes"):
        print("❌ Failed to populate chart data. Please check the error above.")
        return
    
    # Step 5: Verify data
    print("\n✅ Step 5: Verifying imported data...")
    try:
        import sqlite3
        conn = sqlite3.connect('instance/hospital.db')
        c = conn.cursor()
        
        patients = c.execute('SELECT COUNT(*) FROM patient').fetchone()[0]
        doctors = c.execute('SELECT COUNT(*) FROM doctor').fetchone()[0]
        vitals = c.execute('SELECT COUNT(*) FROM vital_signs').fetchone()[0]
        notes = c.execute('SELECT COUNT(*) FROM medical_note').fetchone()[0]
        lab_reports = c.execute('SELECT COUNT(*) FROM lab_report').fetchone()[0]
        
        print(f"\n📊 Data Summary:")
        print(f"   Patients:      {patients}")
        print(f"   Doctors:       {doctors}")
        print(f"   Vital Signs:   {vitals}")
        print(f"   Medical Notes: {notes}")
        print(f"   Lab Reports:   {lab_reports}")
        
        conn.close()
        
        # Check if we have enough data
        if patients < 1000:
            print(f"\n⚠️  Warning: Only {patients} patients imported. Expected 1,200+")
        if vitals == 0:
            print("\n⚠️  Warning: No vital signs found. Charts will not display data.")
        if notes == 0:
            print("\n⚠️  Warning: No medical notes found. Disease distribution chart will be empty.")
        
        if patients >= 1000 and vitals > 0 and notes > 0:
            print("\n✅ All data imported successfully!")
        else:
            print("\n⚠️  Some data may be missing. Check the warnings above.")
            
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
    
    # Final instructions
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Next Steps:")
    print("  1. Run the application: python run.py")
    print("  2. Open browser: http://localhost:5000")
    print("  3. Login with demo accounts:")
    print("     - Admin:    admin / admin123")
    print("     - Doctor:   dr_smith / doctor123")
    print("     - Patient:  patient1 / patient123")
    print("\n📊 You should now see:")
    print("  ✅ Patient trends chart (heart rate, blood pressure, glucose)")
    print("  ✅ Disease distribution pie chart")
    print("  ✅ All 1,200+ patients in the system")
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

