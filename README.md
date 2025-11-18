# WanderChronicles - Travel Booking Platform

A Django-based travel booking platform where users can plan trips, book destinations, and share travel journals.

## Features

- **User Authentication**: Secure registration, login, and logout functionality
- **Trip Planning**: Interactive trip planning with map integration (Leaflet.js)
- **Destination Booking**: Book from curated travel packages
- **Travel Journals**: Create and share travel experiences with image uploads
- **Booking Management**: View and manage your trip bookings
- **Admin Dashboard**: Full-featured admin panel for managing users and bookings

## Tech Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Maps**: Leaflet.js
- **Date Picker**: Flatpickr
- **Icons**: Font Awesome

## Project Structure

```
django-project-updated/
├── dataapp/              # Main application
│   ├── models.py         # Database models (Journal, TripBooking)
│   ├── views.py          # View functions and business logic
│   ├── urls.py           # URL routing
│   ├── forms.py          # Form definitions
│   ├── admin.py          # Admin panel configuration
│   ├── static/           # Static files (CSS)
│   ├── templates/        # HTML templates
│   └── migrations/       # Database migrations
├── myproject3/            # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── media/                 # User-uploaded files (journals)
├── manage.py              # Django management script
└── db.sqlite3             # SQLite database (not in repo)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd django-project-updated
```

2. **Create a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install django
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create a superuser (for admin access):**
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

6. **Run the development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Key Features Explained

### User Authentication
- Users can register with username, email, and password
- Secure login/logout functionality
- Session-based authentication

### Trip Booking
- **Plan Trip**: Custom trip planning with:
  - Origin and destination selection
  - Date selection (one-way or round trip)
  - Traveler count and cabin class
  - Budget and accommodation preferences
  - Special requests
- **Destination Booking**: Quick booking from curated packages
- All bookings are saved to the database and linked to user accounts

### Travel Journals
- Create travel journals with:
  - Title and description
  - Location
  - Cover image upload
- View recently published journals

### Admin Dashboard
- View all users and their details
- Manage trip bookings (view, edit, filter by status)
- Manage travel journals
- Full CRUD operations

## Database Models

### TripBooking
- Stores complete trip booking information
- Linked to Django User model
- Status tracking (Pending, Confirmed, Cancelled)
- Calculated pricing (package + service fee + taxes)

### Journal
- Travel experience entries
- Image uploads for journal covers
- Location and date tracking

## Development Notes

- The project uses SQLite3 for development (easy to set up)
- Media files are stored in the `media/` directory
- Static files are in `dataapp/static/`
- Admin panel is accessible at `/admin/` after creating a superuser

## Security Considerations

⚠️ **Important**: Before deploying to production:
- Change the `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive settings
- Set up a production database (PostgreSQL recommended)

## License

[Your License Here]

## Author

[Your Name Here]

---

**Note**: This is a development project. For production deployment, additional security measures and optimizations are required.

