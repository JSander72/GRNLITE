# GRNLITE: A Manuscript Beta Reading Platform

GRNLITE is a comprehensive web application that connects authors with beta readers, streamlining the manuscript feedback process. Built with Django and deployed on Render, it provides a professional platform for manuscript review and collaboration.

## Application Architecture

### **Backend Components**

- **Django Framework**: Core web framework with custom user model and authentication
- **Django REST Framework**: RESTful API endpoints for frontend interactions
- **PostgreSQL Database**: Production-ready database with comprehensive data models
- **JWT Authentication**: Secure token-based authentication system
- **Email Verification**: Custom middleware for mandatory email verification
- **File Management**: Secure manuscript and media file handling

### **Key Applications**

- **`my_app`**: Core application containing user management, manuscripts, and beta reader functionality
- **`manuscripts`**: Consolidated manuscript-related models (integrated into my_app)
- **Custom User Model**: Extended Django user with email verification and user types
- **Comprehensive Models**: Authors, beta readers, manuscripts, feedback, resources, and notifications

### **Frontend Interface**

- **Responsive Design**: Modern CSS with custom typography (Playwrite DE Grund Thin)
- **Dashboard System**: Separate author and reader dashboards
- **Template Structure**: Organized HTML templates with reusable components
- **Interactive JavaScript**: Dynamic content loading and form handling

## ✨ Features

### **For Authors**

- **Manuscript Management**: Upload manuscripts with cover art, plot summaries, and keywords
- **Beta Reader Selection**: Browse and select beta readers based on experience and genres
- **Feedback Collection**: Receive structured feedback through customizable questions
- **Project Budgeting**: Set budgets and manage beta reader compensation
- **NDA Support**: Optional NDA requirements for sensitive manuscripts
- **Dashboard Analytics**: Track manuscript status and feedback progress

### **For Beta Readers**

- **Profile Creation**: Showcase experience, genres, and availability
- **Manuscript Discovery**: Browse available manuscripts matching interests
- **Application System**: Apply for beta reading projects with cover letters
- **Structured Feedback**: Provide feedback through guided questions and categories
- **Portfolio Building**: Track completed projects and build reputation

### **Shared Features**

- **Email Verification**: Mandatory email verification for account activation
- **Notifications**: Real-time notifications for project updates
- **Resource Library**: Access to writing guides and templates
- **Secure Authentication**: JWT-based authentication with session management

## Technologies Used

- **Backend**: Django 5.1.4, Django REST Framework 3.15.2
- **Database**: PostgreSQL with psycopg2-binary
- **Authentication**: JWT (djangorestframework-simplejwt), Social Auth
- **File Handling**: Pillow for image processing, python-docx for documents
- **Deployment**: Gunicorn, Whitenoise for static files
- **Frontend**: HTML5, CSS3, JavaScript, responsive design
- **Development**: Black (formatting), Flake8 (linting), Pytest (testing)

## Installation & Setup

### **Prerequisites**

- Python 3.8+
- PostgreSQL
- Git

### **Local Development Setup**

1. **Clone the repository**

   ```bash
   git clone https://github.com/JSander72/GRNLITE.git
   cd GRNLITE
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   DATABASE_URL=postgresql://username:password@localhost:5432/grnlite_db
   
   # Email Configuration (optional for development)
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Set up database**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Testing

### **Run Tests**

```bash
# Run all tests
python manage.py test

# Run with coverage
pytest --cov=my_app

# Run specific test files
python manage.py test my_app.tests
```

### **Code Quality**

```bash
# Format code
black .

# Check linting
flake8

# Check Django configuration
python manage.py check --deploy
```

### **Manual Testing Workflow**

1. **User Registration & Authentication**
   - Register as author/beta reader
   - Verify email functionality
   - Test login/logout

2. **Author Workflow**
   - Submit manuscript with metadata
   - Browse beta readers
   - Review feedback received

3. **Beta Reader Workflow**
   - Create profile with genres
   - Apply for manuscripts
   - Submit structured feedback

## 🌐 Deployment

### **Render Deployment**

The application is configured for deployment on Render with:

- **`render.yaml`**: Service configuration
- **PostgreSQL database**: Managed database service
- **Environment variables**: Secure configuration management
- **Static file serving**: Whitenoise for production static files

### **Environment Variables for Production**

```env
DJANGO_SECRET_KEY=secure-production-key
DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.onrender.com
DATABASE_URL=postgresql://...  # Provided by Render
```

## Project Structure

```
GRNLITE/
├── grnlite/                 # Django project settings
├── my_app/                  # Core application
│   ├── models.py           # Data models (User, Manuscript, Feedback, etc.)
│   ├── views.py            # API and template views
│   ├── serializers.py      # DRF serializers
│   ├── forms.py            # Django forms
│   ├── middleware.py       # Email verification middleware
│   └── migrations/         # Database migrations
├── Templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
├── render.yaml            # Deployment configuration
└── manage.py              # Django management script
```

## Security Features

- **Email Verification**: Mandatory verification before access
- **JWT Authentication**: Secure token-based auth
- **CSRF Protection**: Built-in Django CSRF middleware
- **File Upload Security**: Secure file handling and storage
- **Environment-based Configuration**: Secure secrets management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For questions or issues:

- Create an issue on GitHub
- Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details.
