from django import forms
from .models import Registration, Event, Profile
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[('student', 'Student'), ('working', 'Working Professional')],
        widget=forms.RadioSelect,
        label='Are you a Student or Working Professional?'
    )
    
    class Meta:
        model = Registration
        fields = ['full_name', 'age', 'phone_number', 'email', 'category', 'college_name', 'graduation_year', 'terms_agreed']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Age'}),
            'phone_number': forms.TextInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Email'}),
            'college_name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'College/University Name'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Graduation Year (e.g., 2025)'}),
            'terms_agreed': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }
        labels = {
            'college_name': 'College/University Name',
            'graduation_year': 'Expected Graduation Year',
            'terms_agreed': 'I agree to the Terms and Conditions'
        }


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
        'placeholder': 'Enter a strong password',
        'autocomplete': 'new-password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'placeholder': 'Choose a username',
                'autocomplete': 'off'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'placeholder': 'your@email.com',
                'autocomplete': 'off'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if not username.isalnum() and '_' not in username:
            raise forms.ValidationError('Username can only contain letters, numbers, and underscores.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered. Please use a different email.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match.')
            if len(password) < 6:
                raise forms.ValidationError('Password must be at least 6 characters long.')
        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'short_description', 'description', 'highlights', 'image_url', 'date', 'time', 'location', 'capacity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Event name'}),
            'short_description': forms.Textarea(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Short description', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Full event details', 'rows': 4}),
            'highlights': forms.Textarea(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Event highlights (what makes this special)', 'rows': 2}),
            'image_url': forms.URLInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Image URL or paste image link'}),
            'date': forms.DateInput(attrs={'class': 'border p-2 w-full rounded', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'border p-2 w-full rounded', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Event location/venue'}),
            'capacity': forms.NumberInput(attrs={'class': 'border p-2 w-full rounded', 'placeholder': 'Capacity (number of attendees)'}),
        }

class ProfileForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=[
            ('music', 'Music & Concerts'),
            ('tech', 'Technology & Tech Talks'),
            ('sports', 'Sports & Fitness'),
            ('arts', 'Arts & Culture'),
            ('food', 'Food & Dining'),
            ('business', 'Business & Networking'),
            ('education', 'Education & Learning'),
            ('social', 'Social & Community'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='What events interest you? (Select all that apply)'
    )
    
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'profile_picture', 'role', 'city', 'interests']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Your Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': '+91-XXXXXXXXXX',
                'type': 'tel'
            }),
            'profile_picture': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Profile picture URL (or leave blank)'
            }),
            'role': forms.RadioSelect(),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Your City'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'phone': 'Phone Number (optional)',
            'profile_picture': 'Profile Picture URL (optional)',
            'role': 'What is your role?',
            'city': 'City',
        }