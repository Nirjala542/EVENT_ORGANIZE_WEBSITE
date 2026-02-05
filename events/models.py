from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = [('attendee', 'Attendee'), ('organiser', 'Organiser')]
    CATEGORY_CHOICES = [
        ('music', 'Music & Concerts'),
        ('tech', 'Technology & Tech Talks'),
        ('sports', 'Sports & Fitness'),
        ('arts', 'Arts & Culture'),
        ('food', 'Food & Dining'),
        ('business', 'Business & Networking'),
        ('education', 'Education & Learning'),
        ('social', 'Social & Community'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    profile_picture = models.URLField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    is_organiser = models.BooleanField(default=False)
    city = models.CharField(max_length=100, blank=True)
    interests = models.CharField(max_length=500, blank=True)  # Comma-separated categories
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    highlights = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    organiser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organised_events')
    capacity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Registration(models.Model):
    CATEGORY_CHOICES = [('student', 'Student'), ('working', 'Working Professional')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='student')
    college_name = models.CharField(max_length=200, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    terms_agreed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name or self.user.username} -> {self.event.title}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
