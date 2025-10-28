# Flask Authentication & Recipe Management API ✅

## Overview

A full-stack Flask application featuring **complete authentication and authorization** with session management, user registration, login/logout functionality, and a recipe management system. This project demonstrates secure user authentication patterns using Flask-RESTful, SQLAlchemy, and bcrypt password hashing.

🎉 **Status: COMPLETED** - All 19 tests passing ✅

## Features Implemented

### 🔐 **Authentication System**
- **User Registration** (`POST /signup`) - Create new users with encrypted passwords
- **Auto-Login** (`GET /check_session`) - Persistent session management  
- **User Login** (`POST /login`) - Authenticate with username/password
- **User Logout** (`DELETE /logout`) - Secure session termination

### 🍳 **Recipe Management**
- **View All Recipes** (`GET /recipes`) - Browse all recipes (authenticated users only)
- **Create Recipe** (`POST /recipes`) - Add new recipes with validation (authenticated users only)

### 🛡️ **Security & Validation**
- Bcrypt password hashing for secure authentication
- Session-based authorization protecting all recipe endpoints
- Username uniqueness and presence validation
- Recipe instruction minimum length validation (50+ characters)
- Comprehensive error handling with proper HTTP status codes

## Tech Stack

- **Backend:** Flask, Flask-RESTful, SQLAlchemy, Flask-Migrate
- **Authentication:** Flask-Bcrypt, Flask sessions
- **Database:** SQLite (development)
- **Frontend:** React (pre-configured)
- **Testing:** pytest

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- pipenv

### Setup & Installation

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd flask-iam-putting-it-all-together-lab
pipenv install && pipenv shell
npm install --prefix client
```

2. **Initialize database:**
```bash
cd server
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py  # Populate with sample data
```

3. **Run the application:**
```bash
# Start Flask API (Terminal 1)
cd server
python app.py  # Runs on http://localhost:5555

# Start React frontend (Terminal 2)
npm start --prefix client  # Runs on http://localhost:3000
```

4. **Run tests:**
```bash
cd server
pytest  # All 19 tests should pass ✅
```

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/signup` | Register new user | ❌ |
| `GET` | `/check_session` | Verify active session | ✅ |
| `POST` | `/login` | User authentication | ❌ |
| `DELETE` | `/logout` | End user session | ✅ |

### Recipe Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/recipes` | Get all recipes | ✅ |
| `POST` | `/recipes` | Create new recipe | ✅ |

### Example Usage

**Register a new user:**
```bash
curl -X POST http://localhost:5555/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "chef123", "password": "secret123", "image_url": "https://example.com/avatar.jpg", "bio": "Passionate home cook"}'
```

**Login:**
```bash
curl -X POST http://localhost:5555/login \
  -H "Content-Type: application/json" \
  -d '{"username": "chef123", "password": "secret123"}' \
  -c cookies.txt
```

**Create a recipe:**
```bash
curl -X POST http://localhost:5555/recipes \
  -H "Content-Type: application/json" \
  -d '{"title": "Chocolate Cake", "instructions": "Mix ingredients, bake at 350F for 30 minutes...", "minutes_to_complete": 60}' \
  -b cookies.txt
```

## Database Schema

### User Model
```python
class User:
    id: Integer (Primary Key)
    username: String (Unique, Required)
    _password_hash: String (Bcrypt encrypted)
    image_url: String
    bio: String
    
    # Relationships
    recipes: One-to-Many with Recipe
    
    # Methods
    password_hash: Property (write-only, raises AttributeError on read)
    authenticate(password): Boolean
    to_dict(): Dictionary representation
```

### Recipe Model
```python
class Recipe:
    id: Integer (Primary Key)
    title: String (Required)
    instructions: String (Required, min 50 characters)
    minutes_to_complete: Integer
    user_id: Integer (Foreign Key)
    
    # Relationships
    user: Many-to-One with User
    
    # Methods
    to_dict(): Dictionary representation with nested user data
```

## Implementation Details

### Security Features
- **Password Hashing:** All passwords encrypted using bcrypt before storage
- **Session Management:** Flask sessions for maintaining user authentication state
- **Route Protection:** All recipe endpoints require active user session
- **Input Validation:** Server-side validation for all user inputs

### Error Handling
- `201 Created` - Successful user/recipe creation
- `200 OK` - Successful data retrieval
- `204 No Content` - Successful logout
- `401 Unauthorized` - Authentication required
- `422 Unprocessable Entity` - Validation errors

### Testing
Comprehensive test suite covering:
- ✅ User model validation and authentication
- ✅ Recipe model validation 
- ✅ Signup/Login/Logout flows
- ✅ Session management
- ✅ Protected route authorization
- ✅ Recipe CRUD operations

**Test Results:** 19/19 tests passing ✅

## File Structure
```
flask-iam-putting-it-all-together-lab/
├── server/
│   ├── app.py              # Main Flask application & API routes
│   ├── models.py           # SQLAlchemy User & Recipe models
│   ├── config.py           # Flask & database configuration
│   ├── seed.py             # Database seeding script
│   ├── migrations/         # Database migration files
│   └── testing/           # Test suite
├── client/                # React frontend (pre-configured)
├── README.md             # This documentation
└── requirements files
```

## Development Notes

### Key Learnings Implemented
- **Full-stack authentication flow** with Flask sessions and bcrypt
- **RESTful API design** using Flask-RESTful resources
- **Database relationships** with SQLAlchemy ORM
- **Comprehensive validation** at both model and route levels
- **Test-driven development** ensuring all functionality works correctly

### Future Enhancements
- JWT token authentication for stateless API
- Recipe categories and search functionality
- Image upload for recipes
- User profiles and social features
- Recipe rating and review system

---

## 📝 License

This project is part of the Flatiron School curriculum for learning Flask authentication patterns.

**Status:** ✅ **COMPLETED** - All functionality implemented and tested
