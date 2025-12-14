# Complete Setup Guide

This guide will help you set up the Hospital Management System on your computer and populate it with all the data needed to see charts and analytics.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, if cloning from repository)

## Step 1: Install Dependencies

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv hospital_env

# Activate virtual environment
.\hospital_env\Scripts\Activate.ps1

# Install all required packages
pip install -r requirements.txt
```

### Linux/Mac

```bash
# Create virtual environment
python3 -m venv hospital_env

# Activate virtual environment
source hospital_env/bin/activate

# Install all required packages
pip install -r requirements.txt
```

## Step 2: Generate Sample Data

The project needs CSV files with sample data. If they don't exist, generate them:

```bash
# Make sure you're in the project directory
cd Dv  # or your project folder name

# Generate all CSV files (patients, doctors, lab reports, vital signs, departments)
python sample_data.py
```

This will create:
- `dummy_patients.csv` (1,200+ patients)
- `dummy_doctors.csv` (doctors)
- `dummy_lab_reports.csv` (lab test results)
- `dummy_vital_signs.csv` (vital signs data)
- `dummy_departments.csv` (department statistics)

## Step 3: Initialize Database and Import Data

Run the application once to create the database:

```bash
python run.py
```

Press `Ctrl+C` to stop it after the database is created.

## Step 4: Import All Data into Database

Now import all the data into the database. Run these scripts in order:

### 4.1: Import Patients and Doctors

```bash
# This will import all 1,200 patients and doctors
python reimport_all_patients.py
```

This script will:
- Clear existing patient data
- Import all patients from `dummy_patients.csv`
- Show you how many were imported

### 4.2: Populate Chart Data

```bash
# This creates vital signs and medical notes needed for charts
python populate_chart_data.py
```

This script will:
- Create medical notes from patient diagnoses (for disease distribution chart)
- Generate vital signs records (for patient trends chart)
- Show progress and final counts

**Expected Output:**
```
✅ Data population complete!
   Medical Notes created: 1200
   Vital Signs records created: ~9000
   Total Vital Signs in DB: ~9000
   Total Medical Notes in DB: 1200
```

### 4.3: Import Lab Reports (Optional)

If you want lab reports data:

```bash
# Import lab reports from CSV
python -c "from app import app, db, import_lab_reports_from_csv; app.app_context().push(); print(f'Imported: {import_lab_reports_from_csv(\"dummy_lab_reports.csv\")} lab reports')"
```

Or use the Lab Technician dashboard to upload `dummy_lab_reports.csv` via the web interface.

## Step 5: Verify Data

Check that all data is imported:

```bash
python -c "import sqlite3; conn = sqlite3.connect('instance/hospital.db'); c = conn.cursor(); print('Patients:', c.execute('SELECT COUNT(*) FROM patient').fetchone()[0]); print('Doctors:', c.execute('SELECT COUNT(*) FROM doctor').fetchone()[0]); print('Vital Signs:', c.execute('SELECT COUNT(*) FROM vital_signs').fetchone()[0]); print('Medical Notes:', c.execute('SELECT COUNT(*) FROM medical_note').fetchone()[0]); print('Lab Reports:', c.execute('SELECT COUNT(*) FROM lab_report').fetchone()[0]); conn.close()"
```

You should see:
- Patients: 1200
- Doctors: (varies, depends on dummy_doctors.csv)
- Vital Signs: ~9000
- Medical Notes: 1200
- Lab Reports: (varies)

## Step 6: Run the Application

```bash
# Make sure virtual environment is activated
python run.py
```

The application will start on `http://localhost:5000`

## Step 7: Login and View Data

### Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Doctor | dr_smith | doctor123 |
| Patient | patient1 | patient123 |

### What You Should See

1. **Admin Dashboard** (`/admin`):
   - Patient trends chart (heart rate, blood pressure, glucose)
   - Disease distribution pie chart
   - Department performance charts
   - Patient list (1,200 patients)

2. **Doctor Dashboard** (`/doctor`):
   - Patient health trends visualization
   - Assigned patients list
   - Medical notes management

3. **Lab Technician Dashboard** (`/lab`):
   - Upload CSV button for lab reports
   - Lab statistics
   - Recent reports table

## Quick Setup Script (All-in-One)

For convenience, here's a script that does everything:

```bash
# Save this as setup.sh (Linux/Mac) or setup.ps1 (Windows)

# Windows PowerShell (setup.ps1)
python -m venv hospital_env
.\hospital_env\Scripts\Activate.ps1
pip install -r requirements.txt
python sample_data.py
python run.py
# Press Ctrl+C after database is created
python reimport_all_patients.py
python populate_chart_data.py
python run.py
```

## Troubleshooting

### Charts Show "No Data Available"

1. Make sure you ran `populate_chart_data.py`:
   ```bash
   python populate_chart_data.py
   ```

2. Check if data exists:
   ```bash
   python -c "import sqlite3; conn = sqlite3.connect('instance/hospital.db'); c = conn.cursor(); print('Vital Signs:', c.execute('SELECT COUNT(*) FROM vital_signs').fetchone()[0]); print('Medical Notes:', c.execute('SELECT COUNT(*) FROM medical_note').fetchone()[0]); conn.close()"
   ```

3. If counts are 0, re-run `populate_chart_data.py`

### Only 234 Patients Showing

1. Run the re-import script:
   ```bash
   python reimport_all_patients.py
   ```

2. This will clear and re-import all 1,200 patients

### Import Errors

1. Make sure CSV files exist:
   ```bash
   ls dummy_*.csv  # Linux/Mac
   dir dummy_*.csv  # Windows
   ```

2. If missing, generate them:
   ```bash
   python sample_data.py
   ```

### Database Locked Error

1. Make sure the Flask app is not running
2. Close any database viewers
3. Try again

## File Structure After Setup

```
Dv/
├── hospital_env/          # Virtual environment
├── instance/
│   └── hospital.db       # SQLite database (created automatically)
├── templates/            # HTML templates
├── app.py                # Main Flask application
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── sample_data.py        # Generate CSV files
├── reimport_all_patients.py  # Import patients
├── populate_chart_data.py    # Create chart data
├── dummy_patients.csv     # Patient data (1,200 rows)
├── dummy_doctors.csv      # Doctor data
├── dummy_lab_reports.csv  # Lab reports
├── dummy_vital_signs.csv  # Vital signs (for reference)
└── dummy_departments.csv  # Department stats
```

## Summary Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV files generated (`python sample_data.py`)
- [ ] Database initialized (run `python run.py` once)
- [ ] Patients imported (`python reimport_all_patients.py`)
- [ ] Chart data populated (`python populate_chart_data.py`)
- [ ] Application running (`python run.py`)
- [ ] Can login and see charts with data

## Need Help?

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all CSV files exist and have data
3. Check database file exists in `instance/hospital.db`
4. Make sure virtual environment is activated
5. Try deleting `instance/hospital.db` and starting fresh

---

**Note**: The first time you run the application, it may take a minute to import all data. Be patient!

