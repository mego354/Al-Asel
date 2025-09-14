#!/usr/bin/env python3
"""
Environment setup script for Al-Asel Django app
This script helps set up the environment for both development and production
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Django Environment Configuration\n")
            f.write("DJANGO_ENVIRONMENT=development\n")
            f.write("SECRET_KEY=django-insecure-hyv7&3ft0xp$u!0*z-n^q%&mt-oh*nj53o9onh5yap83^%94b*\n")
            f.write("\n# Email Configuration (for production)\n")
            f.write("# EMAIL_HOST=smtp.gmail.com\n")
            f.write("# EMAIL_PORT=587\n")
            f.write("# EMAIL_HOST_USER=your-email@gmail.com\n")
            f.write("# EMAIL_HOST_PASSWORD=your-app-password\n")
            f.write("# DEFAULT_FROM_EMAIL=noreply@yourdomain.com\n")
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def create_logs_directory():
    """Create logs directory if it doesn't exist"""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        print("Creating logs directory...")
        logs_dir.mkdir()
        print("✅ logs directory created")
    else:
        print("✅ logs directory already exists")

def install_requirements():
    """Install Python requirements"""
    print("Installing requirements...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_migrations():
    """Run Django migrations"""
    print("Running migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running migrations: {e}")
        return False
    return True

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Static files collected successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error collecting static files: {e}")
        return False
    return True

def create_superuser():
    """Create superuser if it doesn't exist"""
    print("Checking for superuser...")
    try:
        # Check if superuser exists
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            'from django.contrib.auth import get_user_model; User = get_user_model(); print("Superuser exists" if User.objects.filter(is_superuser=True).exists() else "No superuser")'
        ], capture_output=True, text=True, check=True)
        
        if "No superuser" in result.stdout:
            print("Creating superuser...")
            print("Please enter the following information:")
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
            print("✅ Superuser created successfully")
        else:
            print("✅ Superuser already exists")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating superuser: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Al-Asel Django App...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Creating environment file", create_env_file),
        ("Creating logs directory", create_logs_directory),
        ("Installing requirements", install_requirements),
        ("Running migrations", run_migrations),
        ("Collecting static files", collect_static),
        ("Creating superuser", create_superuser),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo run the development server:")
    print("  python manage.py runserver")
    print("\nTo run in production mode:")
    print("  export DJANGO_ENVIRONMENT=production")
    print("  python manage.py runserver")
    print("\nFor deployment instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main()
