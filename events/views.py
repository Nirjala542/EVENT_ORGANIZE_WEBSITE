from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration, Profile, Testimonial
from .forms import RegistrationForm, SignupForm, EventForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .chatbot import EventsChatbot


def index(request):
    events = Event.objects.filter(is_published=True).order_by('date')[:8]
    testimonials = Testimonial.objects.order_by('-created_at')[:3]
    latest = Event.objects.filter(is_published=True).order_by('-created_at')[:6]
    return render(request, 'events/index.html', {'events': events, 'testimonials': testimonials, 'latest': latest})


def event_list(request):
    qs = Event.objects.filter(is_published=True).order_by('date')
    q = request.GET.get('q')
    date = request.GET.get('date')
    location = request.GET.get('location')
    if q:
        qs = qs.filter(title__icontains=q)
    if date:
        qs = qs.filter(date=date)
    if location:
        qs = qs.filter(location__icontains=location)
    return render(request, 'events/event_list.html', {'events': qs})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    # contact form handling
    if request.method == 'POST' and request.POST.get('contact_submit'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        full_message = f'Contact from {name} <{email}>:\n\n{message}'
        recipient = []
        if event.organiser and event.organiser.email:
            recipient = [event.organiser.email]
        else:
            recipient = [request.site_settings.EMAIL_HOST_USER] if hasattr(request, 'site_settings') else [request.user.email if request.user.is_authenticated else 'no-reply@example.com']
        send_mail(
            f'Contact about {event.title}',
            full_message,
            'no-reply@example.com',
            recipient,
            fail_silently=True,
        )
        messages.success(request, 'Message sent to the organiser (console in dev).')
        return redirect('events:event_detail', slug=slug)

    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def register_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    existing = Registration.objects.filter(user=request.user, event=event, cancelled=False).first()
    if existing:
        messages.info(request, 'You are already registered for this event.')
        return redirect('events:event_detail', slug=slug)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.event = event
            reg.save()
            # send confirmation email
            send_mail(
                'Registered Successfully',
                f'You are registered for {event.title}.',
                'no-reply@example.com',
                [reg.email],
                fail_silently=True,
            )
            messages.success(request, 'Registered successfully. Confirmation email sent.')
            return redirect('events:profile')
    else:
        form = RegistrationForm()

    return render(request, 'events/register.html', {'event': event, 'form': form})


def signup_view(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password']
            )
            
            profile_data = profile_form.cleaned_data
            interests_list = profile_data.get('interests', [])
            interests_str = ','.join(interests_list) if interests_list else ''
            
            profile = Profile.objects.create(
                user=user,
                full_name=profile_data.get('full_name', ''),
                phone=profile_data.get('phone', ''),
                profile_picture=profile_data.get('profile_picture', ''),
                role=profile_data.get('role', 'attendee'),
                city=profile_data.get('city', ''),
                interests=interests_str
            )
            
            # If user selected organiser role, set is_organiser flag
            if profile_data.get('role') == 'organiser':
                profile.is_organiser = True
                profile.save()
            
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Book-My-Event!')
            return redirect('events:index')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        user_form = SignupForm()
        profile_form = ProfileForm()
    
    return render(request, 'events/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('events:index')
        messages.error(request, 'Invalid credentials')
    return render(request, 'events/login.html')


def logout_view(request):
    logout(request)
    return redirect('events:index')


@login_required
def profile_view(request):
    regs = Registration.objects.filter(user=request.user)
    wishlist = []
    return render(request, 'events/profile.html', {'regs': regs, 'wishlist': wishlist})


def gallery_view(request):
    return render(request, 'events/gallery.html')


def community_view(request):
    return render(request, 'events/community.html')


def support_view(request):
    return render(request, 'events/support.html')


def privacy_view(request):
    return render(request, 'events/privacy.html')


def terms_view(request):
    return render(request, 'events/terms.html')


def organiser_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('events:login')
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_organiser:
        return render(request, 'events/organiser_dashboard.html', {'allowed': False})
    events = request.user.organised_events.all()
    return render(request, 'events/organiser_dashboard.html', {'allowed': True, 'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organiser = request.user
            event.is_published = True
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


# Chatbot views
@csrf_exempt
@require_http_methods(["POST"])
def chatbot_response(request):
    """API endpoint for chatbot responses"""
    # #region agent log - Log at the VERY start, before any try/except
    try:
        from pathlib import Path
        import time as _t
        LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
        LOG_FILE = LOG_DIR / 'debug.log'
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:217","message":"chatbot_response() ENTRY","data":{"method":request.method,"path":getattr(request, "path", None),"content_type":request.META.get("CONTENT_TYPE"),"body_length":len(request.body) if hasattr(request, 'body') else 0}, "timestamp":int(_t.time()*1000)})+'\n')
    except Exception as log_err:
        pass  # Don't let logging break the view
    # #endregion
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        # #region agent log
        try:
            from pathlib import Path
            import time as _t
            LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
            LOG_FILE = LOG_DIR / 'debug.log'
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:230","message":"Parsed request body","data":{"user_message_length":len(user_message),"has_message":bool(user_message)}, "timestamp":int(_t.time()*1000)})+'\n')
        except:
            pass
        # #endregion
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Initialize chatbot
        chatbot = EventsChatbot()

        # #region agent log
        try:
            from pathlib import Path
            import time as _t
            LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
            LOG_FILE = LOG_DIR / 'debug.log'
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:245","message":"Calling chatbot.get_response()","data":{"user_message_length":len(user_message)}, "timestamp":int(_t.time()*1000)})+'\n')
        except:
            pass
        # #endregion

        response = chatbot.get_response(user_message)

        # #region agent log
        try:
            from pathlib import Path
            import time as _t
            LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
            LOG_FILE = LOG_DIR / 'debug.log'
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:252","message":"chatbot.get_response() returned","data":{"response_length":len(response) if isinstance(response, str) else None,"response_startswith_sorry":(isinstance(response, str) and response.startswith("Sorry"))}, "timestamp":int(_t.time()*1000)})+'\n')
        except:
            pass
        # #endregion
        
        return JsonResponse({
            'success': True,
            'response': response,
            'message': user_message
        })
    
    except json.JSONDecodeError as je:
        # #region agent log
        try:
            from pathlib import Path
            import time as _t
            LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
            LOG_FILE = LOG_DIR / 'debug.log'
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:268","message":"JSONDecodeError","data":{"error":str(je)}, "timestamp":int(_t.time()*1000)})+'\n')
        except:
            pass
        # #endregion
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # #region agent log
        try:
            from pathlib import Path
            import time as _t
            LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
            LOG_FILE = LOG_DIR / 'debug.log'
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"F","location":"views.py:277","message":"Exception in chatbot_response","data":{"error":str(e),"error_type":type(e).__name__}, "timestamp":int(_t.time()*1000)})+'\n')
        except:
            pass
        # #endregion
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)
