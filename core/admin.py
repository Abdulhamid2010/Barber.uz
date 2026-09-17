from django.contrib import admin
from .models import Profile, BarberProfile, Service, Portfolio, Booking
admin.site.register(Profile)
@admin.register(BarberProfile)
class BarberAdmin(admin.ModelAdmin):
    list_display=("user","region","city","rating","is_verified")
    list_filter=("region","is_verified")
    search_fields=("user__username","user__first_name","user__last_name","city")
admin.site.register(Service)
admin.site.register(Portfolio)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=("user","barber","service","date","time","status")
    list_filter=("status","date")

from .models import PortfolioVideo, Payment, AvailabilitySlot
admin.site.register(PortfolioVideo)
admin.site.register(Payment)
admin.site.register(AvailabilitySlot)
