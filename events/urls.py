from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_list, name='event_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/register/', views.register_event, name='register_event'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('community/', views.community_view, name='community'),
    path('support/', views.support_view, name='support'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('organiser/', views.organiser_dashboard, name='organiser_dashboard'),
    path('create-event/', views.create_event, name='create_event'),
    path('api/chatbot/', views.chatbot_response, name='chatbot_response'),
]
