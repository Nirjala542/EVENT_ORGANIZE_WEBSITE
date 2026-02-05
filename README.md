# 🎉 Book My Event

A modern, full-featured event booking and management platform built with Django. Discover, book, and organize events seamlessly with an AI-powered chatbot assistant.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 Core Features
- **Event Discovery** - Browse featured events with beautiful UI
- **Event Booking** - Easy registration flow with email confirmation
- **User Authentication** - Secure signup, login, and profile management
- **Event Filtering** - Search events by title, date, and location
- **Organizer Dashboard** - Create and manage your events
- **User Profiles** - Track your bookings and event history
- **Event Categories** - Music, Tech, Sports, Arts, Food, Business, Education, Social

### 🤖 AI-Powered Chatbot
- **Gemini AI Integration** - Intelligent event assistant powered by Google Gemini
- **Real-time Responses** - Get instant answers about events and bookings
- **Conversation Context** - Maintains conversation history within sessions
- **Beautiful UI** - Modern chatbot widget with smooth animations

### 📱 Additional Pages
- **Gallery** - Visual showcase of events
- **Community** - Connect with other event-goers
- **Support** - Get help and assistance
- **Privacy & Terms** - Legal pages

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Book_my_event.git
   cd Book_my_event
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key (optional, for chatbot)
   # Get your API key from: https://makersuite.google.com/app/apikey
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📋 Project Structure

```
Book_my_event/
├── book_my_event/          # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── events/                 # Main app
│   ├── models.py           # Database models (Event, Registration, Profile, etc.)
│   ├── views.py            # View functions and API endpoints
│   ├── forms.py            # Django forms
│   ├── chatbot.py          # Gemini AI chatbot integration
│   ├── admin.py            # Django admin configuration
│   ├── templates/          # HTML templates
│   │   └── events/
│   │       ├── index.html
│   │       ├── event_list.html
│   │       ├── event_detail.html
│   │       ├── register.html
│   │       ├── signup.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── create_event.html
│   │       ├── organiser_dashboard.html
│   │       └── chatbot.html
│   └── static/             # Static files (CSS, JS, images)
│       └── events/
│           ├── css/
│           ├── js/
│           └── images/
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── CHATBOT_SETUP.md        # Chatbot setup guide
└── README.md               # This file
```

## 🗄️ Database Models

- **User** - Django's built-in user model
- **Profile** - Extended user profile with role, interests, city
- **Event** - Event details, dates, location, organizer
- **Registration** - User event registrations
- **Wishlist** - User wishlisted events
- **Testimonial** - User testimonials
- **Review** - Event reviews and ratings

## 🔧 Configuration

### Email Configuration

By default, emails are sent to the console. To configure real email sending, update `book_my_event/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Chatbot Setup

For detailed chatbot setup instructions, see [CHATBOT_SETUP.md](CHATBOT_SETUP.md).

Quick setup:
1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file: `GEMINI_API_KEY=your_key_here`
3. Restart the Django server

## 🎨 Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Tailwind CSS (via CDN)
- **AI**: Google Gemini API (for chatbot)
- **Python Packages**:
  - `google-generativeai` - Gemini AI integration
  - `python-dotenv` - Environment variable management

## 📝 Usage

### For Event Attendees

1. **Sign Up** - Create an account at `/signup/`
2. **Browse Events** - Explore events at `/events/`
3. **Filter Events** - Use search, date, and location filters
4. **Register** - Click "Register" on any event page
5. **View Profile** - Check your bookings at `/profile/`
6. **Chat with AI** - Click the chatbot icon for help

### For Event Organizers

1. **Sign Up as Organizer** - Select "Organizer" role during signup
2. **Create Events** - Go to `/create-event/` to add new events
3. **Manage Events** - View and manage your events at `/organiser-dashboard/`
4. **Track Registrations** - See who registered for your events

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file** - It contains sensitive API keys
- ⚠️ **Change SECRET_KEY** - Update `SECRET_KEY` in `settings.py` for production
- ⚠️ **Set DEBUG = False** - In production environments
- ⚠️ **Configure ALLOWED_HOSTS** - Add your domain in production
- ⚠️ **Use HTTPS** - Always use HTTPS in production

## 🧪 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Creating Fake Events (for testing)
```bash
python create_fake_events.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django community for the excellent framework
- Google for the Gemini AI API
- Tailwind CSS for the beautiful styling framework
- All contributors and users of this project

## 📞 Support

For support, email support@bookmyevent.com or open an issue in the GitHub repository.

## 🔮 Future Enhancements

- [ ] Payment integration
- [ ] Email notifications
- [ ] Social media sharing
- [ ] Event recommendations based on user interests
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Event calendar view
- [ ] QR code check-in system

---

⭐ If you like this project, please give it a star on GitHub!
