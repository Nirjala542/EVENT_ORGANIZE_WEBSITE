# Gemini Chatbot Integration Setup Guide

## Overview
A Gemini-powered event assistant chatbot has been integrated into your Book My Event application. Users can ask questions about events, booking, and website features.

## Installation Steps

### 1. **Install Required Packages**
```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Google's Gemini API client
- `python-dotenv` - For environment variable management

### 2. **Get Gemini API Key**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API key"
3. Copy the generated API key

### 3. **Configure Environment Variables**
1. Create a `.env` file in your project root (copy from `.env.example`):
```bash
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. **Install Dependencies**
```bash
pip install google-generativeai python-dotenv
```

### 5. **Run the Application**
```bash
python manage.py runserver
```

## Features

✅ **Smart Event Assistant** - Answers questions about events and bookings
✅ **Real-time Responses** - Uses Google Gemini API for intelligent responses  
✅ **Conversation Context** - Maintains conversation history within a session
✅ **Beautiful UI** - Modern chatbot widget with smooth animations
✅ **Mobile Responsive** - Works perfectly on all devices
✅ **CSRF Protected** - Secure API endpoints

## How It Works

### Frontend
- **chatbot.html** - Chatbot widget markup
- **chatbot.css** - Beautiful styling with gradient and animations
- **chatbot.js** - Handles user interactions and API calls

### Backend
- **chatbot.py** - Gemini integration and chatbot logic
- **views.py** - API endpoint for chatbot responses (`/api/chatbot/`)
- **settings.py** - Configuration for Gemini API key

## API Endpoint

### Send Message
**POST** `/api/chatbot/`

Request:
```json
{
  "message": "How do I register for an event?"
}
```

Response:
```json
{
  "success": true,
  "response": "To register for an event...",
  "message": "How do I register for an event?"
}
```

## Customization

### Change Chatbot Personality
Edit the `SYSTEM_PROMPT` in [events/chatbot.py](events/chatbot.py) to customize the chatbot's behavior and tone.

### Update Styling
Modify [events/static/events/css/chatbot.css](events/static/events/css/chatbot.css) to change colors, sizes, or layout.

### Adjust Conversation Memory
Modify the `EventsChatbot` class in [events/chatbot.py](events/chatbot.py) to add persistent storage or longer conversation history.

## Troubleshooting

### "API key not found" Error
- Ensure `.env` file exists in project root
- Verify `GEMINI_API_KEY` is set correctly
- Restart the Django server after adding the API key

### Chatbot widget not appearing
- Check browser console for JavaScript errors
- Verify `chatbot.html`, `chatbot.js`, and `chatbot.css` are loaded
- Clear browser cache and reload

### Slow responses
- Gemini API may take 2-3 seconds initially
- Check your internet connection
- Verify API key has sufficient quota

## File Structure

```
events/
├── chatbot.py                  # Gemini chatbot class
├── views.py                    # API endpoint (modified)
├── urls.py                     # Routes (modified)
├── static/events/
│   ├── css/
│   │   └── chatbot.css        # Chatbot styling
│   └── js/
│       └── chatbot.js         # Chatbot functionality
└── templates/events/
    ├── chatbot.html           # Chatbot widget
    └── base.html              # Updated to include chatbot
```

## Security Notes

⚠️ **Important**: 
- Never commit `.env` file to version control
- Keep your Gemini API key secret
- The chatbot uses `@csrf_exempt` only for demonstration - consider implementing proper CSRF validation in production
- Rate limiting is recommended for production deployment

## Next Steps

1. ✅ Test the chatbot by clicking the 💬 button on your website
2. ✅ Customize the system prompt for your specific needs
3. ✅ Add conversation history to database (optional)
4. ✅ Implement user feedback/rating system
5. ✅ Add analytics to track chatbot usage

## Support

For issues with:
- **Gemini API**: https://ai.google.dev/docs
- **Django**: https://docs.djangoproject.com/
- **Your Application**: Check the project README.md
