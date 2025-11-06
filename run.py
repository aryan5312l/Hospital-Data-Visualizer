#!/usr/bin/env python3
"""
Hospital Management System - Startup Script
Run this script to start the application
"""

import os
import sys
from app import app, db

def main():
    """Main function to start the application"""
    print("🏥 Hospital Management System")
    print("=" * 40)
    print("Starting application...")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
        
        # Check if sample data exists
        from app import User
        if User.query.count() == 0:
            print("📊 Creating sample data...")
            from app import create_sample_data
            create_sample_data()
            print("✅ Sample data created")
        else:
            print("ℹ️  Sample data already exists")
    
    print("\n🚀 Application is ready!")
    print("📍 Access the application at: http://localhost:5000")
    print("\n👤 Demo Accounts:")
    print("   Admin:    admin / admin123")
    print("   Doctor:   dr_smith / doctor123")
    print("   Patient:  patient1 / patient123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
