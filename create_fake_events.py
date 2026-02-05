#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_my_event.settings")
django.setup()

from django.contrib.auth.models import User
from events.models import Event, Profile
from datetime import datetime, timedelta
from django.utils.text import slugify

# Get or create a test user for events
user, created = User.objects.get_or_create(
    username='eventcreator',
    defaults={'email': 'events@bookmyevent.com', 'first_name': 'Event', 'last_name': 'Creator'}
)

# Create profile if not exists
Profile.objects.get_or_create(user=user)

# Create fake events
events_data = [
    {
        'title': 'Tech Conference 2026',
        'short_description': 'Annual tech conference featuring latest innovations',
        'description': 'Join us for the biggest tech conference of 2026. Meet industry leaders, attend workshops, and network with professionals.',
        'highlights': 'Keynote speakers, Workshops, Networking, Expo',
        'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=10),
        'time': '09:00:00',
        'location': 'Mumbai, India',
        'capacity': 500,
        'organiser': user,
        'is_published': True
    },
    {
        'title': 'Live Music Festival',
        'short_description': 'Amazing artists performing live at the grand amphitheater',
        'description': 'Experience live music from your favorite artists. Three days of non-stop entertainment with food trucks and entertainment.',
        'highlights': 'Live bands, Food festival, VIP seating, Parking',
        'image_url': 'https://images.unsplash.com/photo-1540575467063-178f50902556?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=20),
        'time': '18:00:00',
        'location': 'Bangalore, India',
        'capacity': 2000,
        'organiser': user,
        'is_published': True
    },
    {
        'title': 'Art Workshop - Painting Basics',
        'short_description': 'Learn painting from professional artists in a fun environment',
        'description': 'Perfect for beginners! Learn basic painting techniques, color theory, and create your first masterpiece.',
        'highlights': 'Professional instructors, Art supplies included, Certificate, Small group',
        'image_url': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=7),
        'time': '10:00:00',
        'location': 'Delhi, India',
        'capacity': 30,
        'organiser': user,
        'is_published': True
    },
    {
        'title': 'Startup Networking Meetup',
        'short_description': 'Connect with founders, investors, and tech enthusiasts',
        'description': 'Monthly meetup for startup founders and investors. Share ideas, get feedback, and build connections.',
        'highlights': 'Free networking, Pitch opportunities, Investor panel, Refreshments',
        'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=5),
        'time': '17:00:00',
        'location': 'Bangalore, India',
        'capacity': 100,
        'organiser': user,
        'is_published': True
    },
    {
        'title': 'Yoga & Wellness Retreat',
        'short_description': 'Relaxing weekend retreat with yoga and wellness sessions',
        'description': 'Escape the hustle and bustle. Join us for a wellness retreat with yoga, meditation, healthy meals, and nature.',
        'highlights': 'Yoga classes, Meditation, Healthy meals, Nature walks, Spa',
        'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=15),
        'time': '07:00:00',
        'location': 'Goa, India',
        'capacity': 50,
        'organiser': user,
        'is_published': True
    },
    {
        'title': 'Food Festival - Street Food Extravaganza',
        'short_description': 'Taste authentic cuisines from around the world',
        'description': 'Experience food from 50+ stalls representing cuisines from across India and the world.',
        'highlights': 'Food stalls, Live cooking demos, Music, Kids zone, Parking',
        'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561501?w=600&h=400&fit=crop',
        'date': datetime.now().date() + timedelta(days=25),
        'time': '11:00:00',
        'location': 'Pune, India',
        'capacity': 3000,
        'organiser': user,
        'is_published': True
    },
]

# Create events
for event_data in events_data:
    slug = slugify(event_data['title'])
    event, created = Event.objects.get_or_create(
        slug=slug,
        defaults=event_data
    )
    if created:
        print(f"✅ Created: {event.title}")
    else:
        print(f"⏭️  Already exists: {event.title}")

print("\n✨ Fake events created successfully!")
