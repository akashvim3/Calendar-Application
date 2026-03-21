# Calendar Application

A comprehensive Django-based web application featuring calendar management, task tracking, email integration, chat functionality, notifications, and AI assistance.

## Features

- **Calendar Management**: Create, edit, and manage events with recurring options
- **Task Tracking**: Organize tasks with priorities, due dates, and categories
- **Email Integration**: Send, receive, and manage emails within the application
- **Real-time Chat**: Communicate with team members through integrated chat
- **Notification System**: Get alerts for upcoming events, tasks, and messages
- **AI Assistant**: Intelligent assistance for scheduling and productivity
- **User Authentication**: Secure login, registration, and profile management
- **Responsive Design**: Works on desktop and mobile devices
- **Admin Panel**: Django admin interface for easy management
- **RESTful APIs**: Backend APIs for frontend consumption

## Technology Stack

- **Backend**: Django 4.x
- **Frontend**: HTML5, CSS3, JavaScript (with Bootstrap)
- **Database**: SQLite (development), configurable for PostgreSQL/MySQL
- **Real-time Communication**: Django Channels with WebSockets
- **Authentication**: Django Allauth
- **API**: Django REST Framework
- **Deployment**: Docker-ready, Gunicorn, Nginx

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git
- Virtual environment tool (venv or virtualenv)

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/akashvim3/calendar-app.git
   cd calendar-app
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

### Running the Application

```bash
# Start the development server
python manage.py runserver

# For production, use Gunicorn
gunicorn ai_assistant.wsgi:application --bind 0.0.0.0:8000
```

Visit `http://localhost:8000` in your browser.

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of hosts
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `EMAIL_BACKEND`: Email service configuration
- `REDIS_URL`: For Django Channels (if using Redis)
- `OPENAI_API_KEY`: For AI assistant features

### Django Settings

Settings are located in `ai_assistant/settings.py`:

- Database configuration
- Installed apps
- Middleware
- Template configuration
- Static and media files
- Authentication backends

## API Endpoints

The application provides RESTful APIs for integration:

- `/api/accounts/` - User management
- `/api/calendar/` - Events and calendars
- `/api/tasks/` - Task management
- `/api/email/` - Email operations
- `/api/chat/` - Chat functionality
- `/api/notifications/` - Notification system
- `/api/ai/` - AI assistant endpoints

API documentation is available at `/api/docs/` when DEBUG=True.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Software Foundation
- Bootstrap contributors
- Open-source libraries used in this project
- All contributors who have helped shape this application

## Contact

Project Link: <https://github.com/akashvim3/calendar-app>
