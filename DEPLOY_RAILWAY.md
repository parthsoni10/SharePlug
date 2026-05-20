# Railway.app deployment guide for SharePlug

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Create a new project

## Step 2: Deploy from GitHub

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select SharePlug repository
5. Railway auto-detects Django and sets up

## Step 3: Add PostgreSQL Database

1. In Railway, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically adds DATABASE_URL to environment

## Step 4: Configure Environment Variables

In the Variables tab, add:
```
DEBUG=False
SECRET_KEY=your-random-secret-key-here (generate a new one)
ALLOWED_HOSTS=your-app-name.railway.app
PYTHON_VERSION=3.11
```

## Step 5: Configure Start Command

1. Go to Deploy tab
2. Set **Start Command** to:
   ```
   python manage.py migrate && gunicorn SharePlug.wsgi:application
   ```

## Step 6: Verify Deployment

1. Wait for deployment to complete (green check)
2. Click "View" to see your live app
3. Check logs for any errors

## Cost on Railway (as of May 2026):
- Free: $5 credit/month
- After that: Pay-as-you-go (~$0.000463/hour for basic)
- PostgreSQL: ~$6-12/month

## Advantages of Railway:
- ✅ Auto-detects Django
- ✅ Free $5 credit
- ✅ Simple UI
- ✅ Built-in PostgreSQL
- ✅ Easy environment variables

## Troubleshooting:
- Check Logs tab for errors
- Common issue: Missing migrations → add to Start Command
- Static files not showing → Run `collectstatic --noinput` in Build Command

## Helpful Links:
- Railway Django docs: https://docs.railway.app/
- Support: https://railway.app/support
