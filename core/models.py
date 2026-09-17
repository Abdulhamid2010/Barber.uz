from django.contrib.auth.models import User
from django.db import models

REGIONS = [
("Toshkent shahri","Toshkent shahri"),("Toshkent viloyati","Toshkent viloyati"),
("Andijon","Andijon"),("Buxoro","Buxoro"),("Farg‘ona","Farg‘ona"),
("Jizzax","Jizzax"),("Xorazm","Xorazm"),("Namangan","Namangan"),
("Navoiy","Navoiy"),("Qashqadaryo","Qashqadaryo"),("Samarqand","Samarqand"),
("Sirdaryo","Sirdaryo"),("Surxondaryo","Surxondaryo"),("Qoraqalpog‘iston","Qoraqalpog‘iston"),
]

class Profile(models.Model):
    ROLE=[("user","User"),("barber","Barber")]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE,default="user")
    avatar=models.ImageField(upload_to="avatars/",blank=True,null=True)
    phone=models.CharField(max_length=30,blank=True)
    def __str__(self): return self.user.username

class BarberProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="barber")
    bio=models.TextField(blank=True)
    region=models.CharField(max_length=60,choices=REGIONS)
    city=models.CharField(max_length=80)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=30)
    rating=models.DecimalField(max_digits=2,decimal_places=1,default=5.0)
    experience=models.PositiveIntegerField(default=1)
    working_hours=models.CharField(max_length=80,default="09:00 — 21:00")
    is_verified=models.BooleanField(default=False)
    is_featured=models.BooleanField(default=False)
    cover=models.ImageField(upload_to="barbers/covers/",blank=True,null=True)
    latitude=models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    longitude=models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    instagram=models.URLField(blank=True)
    telegram=models.URLField(blank=True)
    def __str__(self): return f"{self.user.get_full_name() or self.user.username} — {self.city}"

class Service(models.Model):
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name="services")
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    duration=models.PositiveIntegerField(default=45)
    def __str__(self): return f"{self.name} — {self.price:,} so'm"

class Portfolio(models.Model):
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name="portfolio")
    image=models.ImageField(upload_to="portfolio/")
    title=models.CharField(max_length=120,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    STATUS=[("pending","Kutilmoqda"),("confirmed","Tasdiqlangan"),("cancelled","Bekor qilingan"),("done","Yakunlangan")]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings")
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name="bookings")
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    note=models.CharField(max_length=300,blank=True)
    status=models.CharField(max_length=20,choices=STATUS,default="pending")
    created_at=models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="review")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name="reviews")
    rating=models.PositiveSmallIntegerField(default=5)
    text=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="favorites")
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name="favorited_by")
    class Meta:
        constraints=[models.UniqueConstraint(fields=["user","barber"],name="unique_favorite")]

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    title=models.CharField(max_length=150)
    text=models.CharField(max_length=300)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class BarberSubscription(models.Model):
    PLAN=[("free","Free"),("pro","Pro")]
    barber=models.OneToOneField(BarberProfile,on_delete=models.CASCADE,related_name="subscription")
    plan=models.CharField(max_length=10,choices=PLAN,default="free")
    active_until=models.DateField(blank=True,null=True)
    def __str__(self): return f"{self.barber} — {self.plan}"


class PortfolioVideo(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="portfolio/videos/")
    title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Video #{self.pk}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name="payments")
    booking = models.ForeignKey("Booking", on_delete=models.CASCADE, null=True, blank=True, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=30, default="demo")
    external_id = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider} #{self.pk} — {self.status}"


class AvailabilitySlot(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name="availability_slots")
    weekday = models.PositiveSmallIntegerField()  # Monday=0 ... Sunday=6
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.barber} / {self.weekday} / {self.start_time}-{self.end_time}"
