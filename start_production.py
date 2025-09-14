#!/usr/bin/env python3
"""
Production startup script for Al-Asel Django app
This script sets up the environment and starts the production server
"""

import os
import sys
import subprocess
from pathlib import Path

def set_production_environment():
    """Set production environment variables"""
    os.environ['DJANGO_ENVIRONMENT'] = 'production'
    print("✅ Production environment set")

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import django
        print(f"✅ Django {django.get_version()} installed")
    except ImportError:
        print("❌ Django not installed. Please run: pip install -r requirements.txt")
        return False
    
    try:
        import gunicorn
        print("✅ Gunicorn installed")
    except ImportError:
        print("❌ Gunicorn not installed. Please run: pip install gunicorn")
        return False
    
    return True

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False
    return True

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Static files collected")
    except subprocess.CalledProcessError as e:
        print(f"❌ Static files collection failed: {e}")
        return False
    return True

def start_server():
    """Start the production server"""
    print("Starting production server...")
    try:
        # Use gunicorn for production
        subprocess.run([
            'gunicorn',
            '--bind', '0.0.0.0:8000',
            '--workers', '3',
            '--timeout', '120',
            'asel.wsgi_production:application'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    return True

def main():
    """Main production startup function"""
    print("🚀 Starting Al-Asel Django App in Production Mode...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Setting production environment", set_production_environment),
        ("Checking requirements", check_requirements),
        ("Running migrations", run_migrations),
        ("Collecting static files", collect_static),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Production setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Production setup completed successfully!")
    print("🌐 Starting server on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
