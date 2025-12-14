# Hospital Data Analysis Web Application

Secure, role-based hospital management with interactive analytics (Plotly), data entry, CSV import utilities, and dashboards for Admin, Doctor, Patient, and Lab Technician.

## 🏥 Features

### User Roles & Access Control
- **Admin**: Manage users, view analytics, oversee hospital operations
- **Doctor**: View assigned patients, add medical notes, analyze patient trends
- **Patient**: View medical history, lab reports, upcoming appointments
- **Lab Technician**: Upload test results, manage lab reports

### Data Analytics & Visualizations
- **Patient Health Trends**: Interactive line charts showing vital signs over time
- **Disease Distribution**: Pie charts displaying diagnosis patterns
- **Department Performance**: Bar charts comparing department statistics
- **Real-time Dashboard**: Dynamic analytics for different user roles

### Core Functionality
- Secure JWT-based authentication
- Role-based access control
- Patient management system
- Medical records and notes
- Lab report management
- Appointment scheduling
- Vital signs tracking
- Interactive data visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Quick Setup (Automated)

**For a complete automated setup with all data:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the complete setup script
python setup_complete.py
```

This will:
- ✅ Generate all CSV data files
- ✅ Import 1,200+ patients
- ✅ Create vital signs and medical notes for charts
- ✅ Verify all data is imported

### Manual Setup

**For step-by-step instructions, see [SETUP.md](SETUP.md)**

Quick manual steps:

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate CSV data**
   ```bash
   python sample_data.py
   ```

3. **Import patients and populate chart data**
   ```bash
   python reimport_all_patients.py
   python populate_chart_data.py
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Login with demo accounts (see below)

### Demo Accounts

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | admin | admin123 | Full system access, analytics dashboard |
| Doctor | dr_smith | doctor123 | Patient management, medical notes, trends |
| Patient | patient1 | patient123 | Personal medical records, appointments |
| Lab Tech | (create new) | - | Lab report management |

To create a lab tech quickly (run in browser console after opening `/`):
```javascript
fetch('/api/register', {
  method: 'POST',
  headers: { 'Content-Type':'application/json' },
  body: JSON.stringify({
    role:'lab_tech', username:'lab_asha', email:'lab.asha@example.com', password:'labtech123',
    first_name:'Asha', last_name:'Menon', department:'Pathology', phone:'555-3010', certification:'ASCP-MLS'
  })
}).then(r=>r.json()).then(console.log)
```
Then log in at `/` with `lab_asha` / `labtech123`.

## 📊 Data Analytics Features

### 1. Patient Health Trends
- **Heart Rate Monitoring**: Track heart rate changes over time
- **Blood Pressure Analysis**: Systolic and diastolic trends
- **Glucose Level Tracking**: Diabetes monitoring
- **Temperature Monitoring**: Fever detection and tracking

### 2. Disease Distribution Analysis
- **Diagnosis Patterns**: Most common diseases and conditions
- **Department Analysis**: Patient distribution across departments
- **Treatment Effectiveness**: Recovery rate analysis

### 3. Department Performance Metrics
- **Patient Load**: Number of patients per department
- **Doctor Workload**: Patient assignments and capacity
- **Appointment Statistics**: Scheduling and completion rates

## 🛠️ Technical Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Authentication**: JWT tokens with role-based access
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **API**: RESTful endpoints for all operations

### Frontend
- **Framework**: HTML5, CSS3, JavaScript (ES6+)
- **UI Library**: Bootstrap 5 with custom styling
- **Charts**: Plotly.js for interactive visualizations
- **Responsive**: Mobile-friendly design

### Data Analysis
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static chart generation
- **Seaborn**: Statistical visualizations
- **Plotly**: Interactive web-based charts

## 📁 Project Structure

```
hospital-management-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Login page
│   ├── admin.html        # Admin dashboard
│   ├── doctor.html       # Doctor dashboard
│   ├── patient.html      # Patient dashboard
│   └── lab.html          # Lab technician dashboard
├── dummy_doctors.csv     # Indian doctors
├── dummy_patients.csv    # Indian patients
├── dummy_lab_reports.csv # Example lab results
└── hospital.db           # SQLite database (created automatically)
```

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Dashboards
- `GET /api/dashboard/admin` - Admin dashboard data
- `GET /api/dashboard/doctor` - Doctor dashboard data
- `GET /api/dashboard/patient` - Patient dashboard data

### Analytics
- `GET /api/analytics/patient-trends` - Patient health trends chart
- `GET /api/analytics/disease-distribution` - Disease distribution chart
- `GET /api/analytics/department-performance` - Department performance chart

### Patient Management
- `GET /api/patients` - List all patients
- `POST /api/patients/{id}/vitals` - Add vital signs
- `POST /api/patients/{id}/lab-reports` - Add lab report
- `POST /api/patients/{id}/medical-notes` - Add medical note
 - `POST /api/patients/{id}/assign-doctor` - Assign doctor (Admin/Doctor)

## 🎨 User Interface

### Admin Dashboard
- Hospital statistics overview
- Interactive analytics charts
- Patient management table
- Recent appointments list

### Doctor Dashboard
- Assigned patients list
- Patient health trends visualization
- Medical note management
- Vital signs recording

### Patient Dashboard
- Personal medical history
- Lab reports and results
- Upcoming appointments
- Health summary statistics

### Lab Technician Dashboard
- Lab report creation
- Test result management
- Lab statistics overview
- Recent reports table

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access**: Each role has specific permissions
- **Password Hashing**: Bcrypt for secure password storage
- **CORS Protection**: Cross-origin request security
- **Input Validation**: Server-side data validation

## 📈 Sample Data & Reset/Import

CSV files provided: `dummy_doctors.csv`, `dummy_patients.csv`, `dummy_lab_reports.csv` (Indian names).

To wipe old data and import fresh (Admin only), run in browser console after logging in:
```javascript
fetch('/api/admin/reset-and-import?doctors=dummy_doctors.csv&patients=dummy_patients.csv&labs=dummy_lab_reports.csv', {
  method: 'POST',
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
}).then(r=>r.json()).then(console.log)
```
Reload the dashboards; charts are dynamic and reflect DB data.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Update database configuration in `app.py`
2. Set secure secret keys
3. Configure web server (nginx + gunicorn)
4. Set up SSL certificates
5. Configure environment variables

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
```

## 🔧 Configuration

### Database Configuration
```python
# For PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/hospital'

# For MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/hospital'
```

### Security Configuration
```python
app.config['SECRET_KEY'] = 'your-secure-secret-key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
```

## 📊 Analytics Examples

### Patient Health Trends
- Heart rate monitoring over time
- Blood pressure trend analysis
- Glucose level tracking
- Temperature variations

### Disease Distribution
- Most common diagnoses
- Seasonal disease patterns
- Age-group specific conditions
- Treatment effectiveness

### Department Performance
- Patient load distribution
- Doctor workload analysis
- Appointment completion rates
- Resource utilization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the sample data and demo accounts

## 🔮 Future Enhancements

- Real-time notifications
- Mobile app integration
- Advanced reporting features
- Machine learning predictions
- Integration with medical devices
- Multi-language support
- Advanced security features

---

**Note**: This is a demonstration application. For production use, implement additional security measures, data validation, and compliance with healthcare regulations (HIPAA, etc.).

## Troubleshooting

- Charts tiny: hard refresh (Ctrl+F5). `.chart-container` has a minimum height set.
- No charts: import data using the reset/import command above.
- Unauthorized (401/422): token expired; log in again at `/`.
- Lab Analysis empty: ensure `dummy_lab_reports.csv` imported, or add reports on the Lab dashboard.
