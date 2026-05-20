# 🔌 SharePlug - EV Charging Station Finder

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.2.0-darkgreen?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

**Find and book EV charging stations near you with just a few clicks.**

[Features](#features) • [Installation](#installation) • [Architecture](#architecture) • [API](#api-endpoints) • [Deployment](#deployment) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Configuration](#configuration)
7. [How It Works](#how-it-works)
8. [API Endpoints](#api-endpoints)
9. [Database Schema](#database-schema)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)

---

## 📱 Overview

**SharePlug** is a comprehensive web application designed to help electric vehicle (EV) owners find and book charging stations across India. The platform connects EV owners with charging station operators, making it easy to locate nearby stations, check availability, and make advance bookings.

### Problem Statement
- EV owners struggle to find nearby charging stations
- No centralized platform for booking slots
- Limited information about charger types and pricing
- Difficulty in comparing stations

### Solution
SharePlug provides:
- Interactive map-based station discovery
- Real-time availability tracking
- Easy slot booking system
- User ratings and reviews
- Station management dashboard for operators
- Admin analytics and oversight

---

## ✨ Features

### For Users (EV Owners)
- 🗺️ **Interactive Map**: Browse nearby charging stations on an interactive Leaflet map
- 🔍 **Advanced Search**: Filter stations by location, charger type, and availability
- 📍 **Geolocation**: Find nearest station using GPS
- ⭐ **Ratings & Reviews**: See station ratings and read reviews from other users
- 🔖 **Bookmarks**: Save favorite stations for quick access
- ✅ **Check-in**: Log when you arrive at a station
- 📅 **Booking**: Reserve charging slots in advance
- 🖼️ **Photo Upload**: Upload photos of stations
- 👤 **User Profiles**: Manage account and view booking history

### For Business (Station Owners)
- 📝 **Station Registration**: Register new EV charging stations
- 💼 **Dashboard**: Manage station details and charger information
- 📊 **Booking Management**: View and manage customer bookings
- 💰 **Pricing Setup**: Configure charging rates
- 🔋 **Charger Management**: Add multiple chargers with different specifications

### For Admin
- 📈 **Analytics Dashboard**: View platform statistics and trends
- ✅ **Registration Approval**: Review and approve new station registrations
- 👥 **User Management**: Manage all users and permissions
- 🛠️ **Station Management**: Control station visibility and status
- 📅 **Booking Oversight**: Monitor all bookings on the platform
- 📊 **Reporting**: Generate reports on platform activity

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.11+ | Programming language |
| **Django** | 4.2.0 | Web framework |
| **Django ORM** | Built-in | Database abstraction layer |
| **Gunicorn** | 21.2.0 | WSGI HTTP server |
| **Whitenoise** | 6.5.0 | Static file serving |

### Database & Storage
| Technology | Version | Purpose |
|-----------|---------|---------|
| **SQLite** | Latest | Local development database |
| **PostgreSQL** | 15+ | Production database |
| **Pillow** | 10.0.0 | Image processing (station photos) |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **HTML5** | Latest | Markup |
| **CSS3** | Latest | Styling (custom + Flexbox/Grid) |
| **JavaScript (Vanilla)** | ES6+ | Interactivity |
| **Leaflet.js** | 1.9.4 | Interactive maps |
| **Leaflet Marker Cluster** | 1.5.3 | Map markers clustering |
| **Nominatim API** | Latest | Geolocation & search |

### Utilities
| Library | Version | Purpose |
|---------|---------|---------|
| **geopy** | 2.3.0 | Distance calculation (geodesic) |
| **python-decouple** | 3.8 | Environment variables |
| **dj-database-url** | 2.1.0 | Database URL parsing |
| **psycopg2-binary** | 2.9.7 | PostgreSQL adapter |

### Development Tools
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **GitHub** | Repository hosting |
| **VS Code** | Code editor |
| **SQLite Browser** | Database inspection |

---

## 📂 Project Structure

```
SharePlug/
├── SharePlug/                 # Main project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI entry point
│   ├── views.py              # Common views
│   └── templates/
│       ├── base.html         # Base template
│       ├── home.html         # Map view
│       ├── login.html        # Login page
│       ├── register.html     # Registration page
│       ├── bookmarks.html    # Saved stations
│       ├── station_detail.html # Station details
│       └── ...
│
├── Map/                       # Map & Station management app
│   ├── models.py             # EVStation, CheckIn, Bookmark, Review, EVStationImage
│   ├── views.py              # Map API, station endpoints
│   ├── urls.py               # Map URL patterns
│   ├── migrations/           # Database migrations
│   └── admin.py              # Django admin config
│
├── accounts/                  # User authentication
│   ├── models.py             # Custom user model (if any)
│   ├── views.py              # Login, register, logout
│   ├── urls.py               # Auth URLs
│   ├── forms.py              # Authentication forms
│   └── templates/
│
├── stations/                  # Station operations
│   ├── models.py             # Station-related models
│   ├── views.py              # Station CRUD, nearest station
│   ├── urls.py               # Station URLs
│   └── admin.py              # Admin interface
│
├── bookings/                  # Booking management
│   ├── models.py             # Booking, TimeSlot models
│   ├── views.py              # Booking CRUD, payment
│   ├── urls.py               # Booking URLs
│   ├── templates/
│   │   ├── booking_page.html      # Booking form
│   │   ├── booking_detail.html    # Booking details
│   │   └── my_bookings.html       # User's bookings
│   └── admin.py
│
├── business/                  # Business (Station Owner) dashboard
│   ├── models.py             # BusinessRegistration model
│   ├── views.py              # Registration, dashboard
│   ├── urls.py               # Business URLs
│   ├── templates/
│   │   ├── landing.html           # Business landing page
│   │   ├── profile_setup.html     # Owner profile
│   │   ├── station_register.html  # Register new station
│   │   └── my_registrations.html  # My stations
│   └── admin.py
│
├── admin_panel/               # Admin dashboard
│   ├── models.py             # Admin settings (if any)
│   ├── views.py              # Analytics, user management
│   ├── urls.py               # Admin URLs
│   ├── templates/
│   │   ├── dashboard.html         # Main admin dashboard
│   │   ├── registrations.html     # Pending approvals
│   │   ├── registration_detail.html # Registration review
│   │   ├── stations.html          # Manage all stations
│   │   ├── users.html             # User list
│   │   ├── bookings.html          # All bookings
│   │   └── analytics.html         # Charts & stats
│   └── admin.py
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── base.css          # Common styles
│   │   ├── home.css          # Map page styles
│   │   ├── bookings.css      # Booking styles
│   │   └── ...
│   ├── js/
│   │   └── home.js           # Map interactions
│   └── images/
│       └── OIP.jpg           # Placeholder image
│
├── media/                     # User-uploaded files
│   ├── stations/             # Station photos
│   └── gallery/              # Station gallery images
│
├── data/                      # Data files
│   └── ev-charging-stations-india-updated.csv # Initial station data
│
├── requirements.txt           # Python dependencies
├── manage.py                 # Django CLI
├── db.sqlite3                # Local database
├── Procfile                  # Deployment config (Heroku/Render)
├── runtime.txt               # Python version
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
└── README.md                 # This file
```

---

## 💾 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool (venv)
- Git
- PostgreSQL (for production) or SQLite (for development)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SharePlug.git
cd SharePlug
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env file with your settings
# Windows: notepad .env
# macOS/Linux: nano .env
```

Add these to `.env`:
```
DEBUG=True
SECRET_KEY=your-random-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=  # Leave empty for SQLite
```

### Step 5: Run Migrations

```bash
# Create database tables
python manage.py migrate

# Load initial data (optional)
python manage.py loaddata initial_data

# Create superuser
python manage.py createsuperuser
```

### Step 6: Collect Static Files (Development)

```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

---

## ⚙️ Configuration

### Database Configuration

**Local Development (SQLite)**
```python
# settings.py (default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL)**
```python
# Set DATABASE_URL environment variable
# Format: postgresql://username:password@localhost:5432/dbname
# The app will auto-detect and use it
```

### Static & Media Files

```python
# static/ directory: CSS, JS, images (app assets)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Collected for production

# media/ directory: User uploads (station photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Email Configuration (Optional)

Add to settings.py for email notifications:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🔄 How It Works

### 1. User Registration & Authentication
```
User → Register → Email Verification → Dashboard
                      ↓
              Django Auth System
              - Login with credentials
              - Session management
              - Password reset
```

### 2. Finding Stations

```
User → Map View → Browse Stations → Click Marker → Station Details
                       ↓
                  Leaflet Map
                  - Real-time clustering
                  - Zoom & pan
                  - Search by location
                  - Filter by distance
```

### 3. Booking Flow

```
User → Select Station → Choose Date/Time → Select Slot → Payment → Booking
                              ↓
                       TimeSlot Model
                       - Check availability
                       - Reserve slot
                       - Send confirmation
```

### 4. Business Registration

```
Operator → Register Station → Add Chargers → Set Pricing → Approval
                                                          ↓
                                               Admin Review
                                               - Verify info
                                               - Approve/Reject
                                               - Go Live
```

### 5. Admin Oversight

```
Admin Dashboard
├── Analytics → Chart.js visualizations
├── Users → List, filter, manage
├── Stations → Approve, activate/deactivate
├── Bookings → View all reservations
└── Reviews → Monitor community feedback
```

---

## 📡 API Endpoints

### Public Endpoints

#### Map & Station Discovery
```
GET  /                                    Home page (map view)
GET  /api/stations/?sw_lat=x&sw_lng=y&ne_lat=z&ne_lng=w    Get stations in bounds
GET  /location/<station_id>/              Station details (JSON)
GET  /get-nearest-station/?latitude=x&longitude=y          Get nearest station
GET  /station/<station_id>/images/        Get station gallery images
```

#### Authentication
```
GET  /login/                              Login page
POST /login/                              Submit login
GET  /register/                           Registration page
POST /register/                           Create account
GET  /logout/                             Logout
```

#### User Features
```
POST /bookmark/<station_id>/              Save/unsave station
POST /checkin/<station_id>/               Check in at station
POST /station/<station_id>/review/        Submit review
POST /station/<station_id>/upload-image/  Upload station photo
```

#### Bookings
```
GET  /bookings/my-bookings/               User's bookings
GET  /book/station/<station_id>/          Booking form
POST /book/station/<station_id>/          Create booking
GET  /bookings/<booking_id>/              Booking details
```

#### Bookmarks
```
GET  /bookmarks/                          Saved stations
GET  /bookmarks/delete/<bookmark_id>/     Remove bookmark
```

### Business Endpoints (Operator)
```
GET  /business/                           Business landing
POST /business/register-station/          Register new station
GET  /business/my-registrations/          View my stations
GET  /business/station/<id>/dashboard/    Station dashboard
POST /business/station/<id>/update/       Update station info
```

### Admin Endpoints (Staff Only)
```
GET  /admin-panel/                        Admin dashboard
GET  /admin-panel/registrations/          Pending approvals
GET  /admin-panel/registrations/<id>/     Review registration
POST /admin-panel/registrations/<id>/approve/    Approve registration
POST /admin-panel/registrations/<id>/reject/     Reject registration
GET  /admin-panel/stations/               Manage all stations
POST /admin-panel/stations/<id>/toggle/   Activate/deactivate
GET  /admin-panel/users/                  User management
GET  /admin-panel/bookings/               All bookings
GET  /admin-panel/analytics/              Dashboard analytics
```

---

## 🗄️ Database Schema

### Core Models

#### EVStation
```python
{
    id: Integer (PK),
    name: String (200),
    state: String (100),
    city: String (100),
    address: Text,
    latitude: Float,
    longitude: Float,
    num_chargers: Integer,
    charger_types: String (200),
    availability_status: Boolean,
    is_active: Boolean,
    image: ImageField,
    owner: ForeignKey(User),
    created_at: DateTime,
    updated_at: DateTime
}
```

#### Booking
```python
{
    id: Integer (PK),
    user: ForeignKey(User),
    station: ForeignKey(EVStation),
    time_slot: ForeignKey(TimeSlot),
    vehicle_number: String (20),
    status: Choice (confirmed/cancelled/pending),
    created_at: DateTime,
    updated_at: DateTime
}
```

#### TimeSlot
```python
{
    id: Integer (PK),
    station: ForeignKey(EVStation),
    date: Date,
    start_time: Time,
    end_time: Time,
    is_available: Boolean,
    price: Decimal
}
```

#### Review
```python
{
    id: Integer (PK),
    user: ForeignKey(User),
    station: ForeignKey(EVStation),
    rating: Integer (1-5),
    comment: Text,
    created_at: DateTime
}
```

#### Bookmark
```python
{
    id: Integer (PK),
    user: ForeignKey(User),
    station: ForeignKey(EVStation),
    created_at: DateTime
}
```

#### CheckIn
```python
{
    id: Integer (PK),
    user: ForeignKey(User),
    station: ForeignKey(EVStation),
    checkin_time: DateTime,
    note: Text
}
```

---

## 🚀 Deployment

### Quick Deploy to Railway (Recommended)

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to https://railway.app
# 3. Click "New Project" → "Deploy from GitHub"
# 4. Select SharePlug repo
# 5. Railway auto-detects and deploys
```

### Deploy to Render

```bash
# Same GitHub push as above
# 1. Go to https://render.com
# 2. Click "New +" → "Web Service"
# 3. Connect GitHub account
# 4. Select repository
# 5. Configure:
#    - Build: pip install -r requirements.txt && python manage.py collectstatic --noinput
#    - Start: gunicorn SharePlug.wsgi:application
```

### Deploy to PythonAnywhere

```bash
# 1. Go to https://pythonanywhere.com
# 2. Sign up and create account
# 3. Upload code or use GitHub integration
# 4. Configure web app with Django
# 5. Set WSGI configuration
# 6. Enable SSL certificate
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Use different port
python manage.py runserver 8001
```

#### Database Errors
```bash
# Reset migrations
python manage.py migrate Map zero
python manage.py migrate

# Create fresh database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings
# Verify staticfiles/ directory exists
```

#### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.11+
```

#### Login Issues
```bash
# Create new superuser
python manage.py createsuperuser

# Check SECRET_KEY in .env
# Verify session settings in settings.py
```

---

## 📊 Performance & Optimization

### Database Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Index frequently queried fields
- Archive old bookings

### Frontend Optimization
- Lazy load images
- Minify CSS/JS
- Use CDN for static files (Cloudinary, AWS S3)
- Cache API responses

### Server Optimization
- Use PostgreSQL instead of SQLite
- Enable GZIP compression
- Set up Redis for caching
- Monitor with Django Debug Toolbar (dev only)

---

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to functions
- Write tests for new features
- Update README if needed

### Areas for Contribution
- [ ] Payment gateway integration (Razorpay, Stripe)
- [ ] Real-time notifications (WebSockets)
- [ ] Mobile app (React Native/Flutter)
- [ ] AI-powered recommendations
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Accessibility improvements

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Email**: your-email@example.com
- **Documentation**: See `/docs` folder
- **FAQ**: Check GitHub Wiki

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Leaflet.js** - Interactive mapping library
- **Django Community** - Web framework and ecosystem
- **Nominatim** - Geolocation service
- **Chart.js** - Data visualization

---

## 📈 Roadmap

### Version 1.1 (Next Release)
- [ ] Payment integration
- [ ] Real-time notifications
- [ ] Advanced filtering
- [ ] User ratings algorithm

### Version 2.0 (Future)
- [ ] Mobile app
- [ ] AI recommendations
- [ ] Social features
- [ ] API for third-party integrations

---

## 👨‍💻 Author

**Your Team/Name**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your-email@example.com

---

<div align="center">

### Made with ❤️ for EV Enthusiasts

**Give this project a ⭐ if you found it helpful!**

</div>
