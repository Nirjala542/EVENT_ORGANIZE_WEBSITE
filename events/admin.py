from django.contrib import admin
from .models import Event, Registration, Profile, Wishlist, Testimonial, Review

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organiser')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Registration)
admin.site.register(Profile)
admin.site.register(Wishlist)
admin.site.register(Testimonial)
admin.site.register(Review)
