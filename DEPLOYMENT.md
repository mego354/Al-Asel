# Al-Asel Django App Deployment Guide

## 🚀 Production Deployment on PythonAnywhere

### 1. Environment Variables Setup

Create a `.env` file in your project root with the following variables:

```bash
# Environment
DJANGO_ENVIRONMENT=production

# Secret Key (generate a new one)
SECRET_KEY=your-new-secret-key-here

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 2. PythonAnywhere Configuration

#### A. Web App Setup
1. Go to the "Web" tab in your PythonAnywhere dashboard
2. Create a new web app
3. Choose "Manual Configuration" and select your Python version
4. Set the source code directory to your project path

#### B. Virtual Environment
```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 asel-env

# Activate virtual environment
workon asel-env

# Install requirements
pip install -r requirements.txt
```

#### C. WSGI Configuration
Update your WSGI file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/path/to/your/project'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable
os.environ['DJANGO_ENVIRONMENT'] = 'production'

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asel.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### D. Static Files Configuration
1. Go to the "Static files" section in the Web tab
2. Add a new mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/path/to/your/project/staticfiles`

#### E. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Security Configuration

#### A. Update ALLOWED_HOSTS
In `settings.py`, update the ALLOWED_HOSTS with your PythonAnywhere domain:
```python
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',
    'www.yourusername.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]
```

#### B. Generate New Secret Key
```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Development Mode

#### A. Local Development
```bash
# Set environment variable
export DJANGO_ENVIRONMENT=development

# Run development server
python manage.py runserver
```

#### B. Environment Variables
Create a `.env` file for development:
```bash
DJANGO_ENVIRONMENT=development
SECRET_KEY=your-development-secret-key
```

### 5. File Structure

```
Al-Asel/
├── asel/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/
│   ├── models.py
│   ├── views_cbv.py
│   ├── urls.py
│   ├── forms.py
│   ├── static/
│   └── templates/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── .env
└── DEPLOYMENT.md
```

### 6. Production Checklist

- [ ] Set `DJANGO_ENVIRONMENT=production`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Generate new `SECRET_KEY`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic`
- [ ] Create superuser account
- [ ] Test all functionality
- [ ] Set up SSL certificate (optional)
- [ ] Configure email settings (optional)

### 7. Monitoring and Logs

Logs are automatically created in the `logs/` directory:
- `logs/django.log` - Application logs
- Check PythonAnywhere error logs in the Web tab

### 8. Backup Strategy

```bash
# Backup database
cp db.sqlite3 backup_db_$(date +%Y%m%d).sqlite3

# Backup media files (if any)
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### 9. Troubleshooting

#### Common Issues:
1. **Static files not loading**: Check static files configuration in PythonAnywhere
2. **Database errors**: Ensure migrations are run
3. **Permission errors**: Check file permissions
4. **Import errors**: Verify virtual environment is activated

#### Debug Mode:
To enable debug mode temporarily, set `DEBUG = True` in settings.py (NOT recommended for production)

### 10. Performance Optimization

- Enable caching in production
- Use CDN for static files (optional)
- Optimize database queries
- Enable gzip compression

## 🔧 Development Mode

For local development, simply run:
```bash
export DJANGO_ENVIRONMENT=development
python manage.py runserver
```

The app will automatically use development settings with debug mode enabled.
