# Render.com deployment guide for SharePlug

## Step 1: Prepare your project on GitHub

1. Create a GitHub repository for your project
2. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/SharePlug.git
   git push -u origin main
   ```

## Step 2: Deploy on Render

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select the SharePlug repository
4. Configure the service:
   - **Name**: shareplug (or any name)
   - **Environment**: Python 3
   - **Region**: Singapore (for Indian users) or closest to you
   - **Branch**: main
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn SharePlug.wsgi:application
     ```

## Step 3: Set Environment Variables

In Render dashboard, go to Environment:
```
DEBUG=False
SECRET_KEY=your-random-secret-key-here
ALLOWED_HOSTS=yourdomain.onrender.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**For PostgreSQL database:**
1. Click "New +" → "PostgreSQL"
2. Name it (e.g., shareplug-db)
3. Copy the connection string and add to DATABASE_URL in Web Service environment

## Step 4: Run Migrations

1. After deployment, add these to your Render service's "Deploy Hooks":
   - **After Deployment**: `python manage.py migrate`

2. Or SSH into your instance and run:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Step 5: Update settings.py

Uncomment or add this at the end of SharePlug/settings.py:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3', conn_max_age=600)
}
```

## Cost on Render (as of May 2026):
- Free tier: Limited but works
- Paid tier: $7+/month for web service + $15+/month for PostgreSQL

## Helpful Links:
- Render Django docs: https://render.com/docs/deploy-django
- Troubleshooting: Check Logs in Render dashboard
