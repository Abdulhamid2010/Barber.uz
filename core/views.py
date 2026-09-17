import os
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg
from django.utils import timezone
from .models import BarberProfile,Service,Booking,Profile,Review,Favorite,Notification,REGIONS,Payment
from .forms import BarberProfileForm, PortfolioVideoForm
from .forms import RegisterForm,BookingForm,ReviewForm

def home(request):
    q=request.GET.get("q",""); region=request.GET.get("region","")
    qs=BarberProfile.objects.select_related("user").all().order_by("-is_featured","-rating")
    if q: qs=qs.filter(Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q)|Q(city__icontains=q))
    if region: qs=qs.filter(region=region)
    return render(request,"home.html",{"barbers":qs[:8],"regions":[x[0] for x in REGIONS]})

def barbers(request):
    q=request.GET.get("q",""); region=request.GET.get("region","")
    qs=BarberProfile.objects.select_related("user").all().order_by("-is_featured","-rating")
    if q: qs=qs.filter(Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q)|Q(city__icontains=q))
    if region: qs=qs.filter(region=region)
    return render(request,"barbers.html",{"barbers":qs,"regions":[x[0] for x in REGIONS]})

def barber_detail(request,pk):
    barber=get_object_or_404(BarberProfile.objects.select_related("user"),pk=pk)
    return render(request,"barber_detail.html",{"barber":barber,"reviews":barber.reviews.select_related("user")[:8]})

@login_required
def book(request,pk):
    barber=get_object_or_404(BarberProfile,pk=pk)
    if request.method=="POST":
        form=BookingForm(request.POST); service=get_object_or_404(Service,pk=request.POST.get("service"),barber=barber)
        if form.is_valid():
            cd=form.cleaned_data
            clash=Booking.objects.filter(barber=barber,date=cd["date"],time=cd["time"],status__in=["pending","confirmed"]).exists()
            if clash: messages.error(request,"Bu vaqt band. Boshqa vaqtni tanlang.")
            elif cd["date"] < timezone.localdate(): messages.error(request,"O‘tgan sanani tanlash mumkin emas.")
            else:
                b=form.save(commit=False); b.user=request.user;b.barber=barber;b.service=service;b.save()
                Notification.objects.create(user=barber.user,title="Yangi bron",text=f"{request.user.get_full_name() or request.user.username} sizga bron yubordi.")
                messages.success(request,"Broningiz yuborildi. Barber tasdiqlashini kuting."); return redirect("dashboard")
    else: form=BookingForm()
    return render(request,"book.html",{"barber":barber,"form":form,"services":barber.services.all()})

@login_required
def favorite(request,pk):
    barber=get_object_or_404(BarberProfile,pk=pk); obj=Favorite.objects.filter(user=request.user,barber=barber)
    if obj.exists(): obj.delete()
    else: Favorite.objects.create(user=request.user,barber=barber)
    return redirect("barber_detail",pk=pk)

@login_required
def review(request,pk):
    booking=get_object_or_404(Booking,pk=pk,user=request.user,status="done")
    if request.method=="POST":
        form=ReviewForm(request.POST)
        if form.is_valid():
            r=form.save(commit=False);r.booking=booking;r.user=request.user;r.barber=booking.barber;r.save()
            avg=Review.objects.filter(barber=booking.barber).aggregate(x=Avg("rating"))["x"]
            booking.barber.rating=round(avg or 5,1);booking.barber.save()
            messages.success(request,"Bahoyingiz qabul qilindi.");return redirect("dashboard")
    else: form=ReviewForm()
    return render(request,"review.html",{"form":form,"booking":booking})

def register_view(request):
    if request.user.is_authenticated:return redirect("dashboard")
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid(): user=form.save();login(request,user);return redirect("dashboard")
    else:form=RegisterForm()
    return render(request,"auth.html",{"form":form,"register":True})

def login_view(request):
    if request.method=="POST":
        user=authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
        if user:login(request,user);return redirect("dashboard")
        messages.error(request,"Login yoki parol noto‘g‘ri.")
    return render(request,"auth.html",{"register":False})

def logout_view(request):logout(request);return redirect("home")

@login_required
def dashboard(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    if profile.role=="barber":
        barber=getattr(request.user,"barber",None)
        bookings=barber.bookings.select_related("user","service").order_by("date","time") if barber else []
        return render(request,"dashboard.html",{"barber":barber,"bookings":bookings,"is_barber":True})
    bookings=request.user.bookings.select_related("barber","service").order_by("-created_at")
    return render(request,"dashboard.html",{"bookings":bookings,"is_barber":False})

@login_required
def booking_action(request,pk,action):
    b=get_object_or_404(Booking,pk=pk,barber__user=request.user)
    if action in dict(Booking.STATUS):
        b.status=action;b.save()
        Notification.objects.create(user=b.user,title="Bron holati",text=f"{b.barber.user.get_full_name() or b.barber.user.username}: {b.get_status_display()}.")
    return redirect("dashboard")


@login_required
def barber_setup(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role != "barber":
        return redirect("dashboard")
    barber, _ = BarberProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = BarberProfileForm(request.POST, request.FILES, instance=barber)
        if form.is_valid():
            form.save()
            messages.success(request, "Barber profilingiz saqlandi.")
            return redirect("dashboard")
    else:
        form = BarberProfileForm(instance=barber)
    return render(request, "barber_setup.html", {"form": form})

@login_required
def add_video(request):
    barber = getattr(request.user, "barber", None)
    if not barber:
        return redirect("barber_setup")
    if request.method == "POST":
        form = PortfolioVideoForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.barber = barber
            item.save()
            messages.success(request, "Video portfolioga qo'shildi.")
            return redirect("dashboard")
    else:
        form = PortfolioVideoForm()
    return render(request, "video_upload.html", {"form": form})

@login_required
def payment_demo(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment, _ = Payment.objects.get_or_create(
        booking=booking,
        user=request.user,
        barber=booking.barber,
        defaults={"amount": booking.service.price, "provider": os.getenv("PAYMENT_PROVIDER", "demo")}
    )
    if request.method == "POST":
        payment.status = "paid"
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at"])
        messages.success(request, "Demo to'lov muvaffaqiyatli belgilandi. Real provider ulanishi uchun PAYMENT_* sozlamalarini to'ldiring.")
        return redirect("dashboard")
    return render(request, "payment.html", {"payment": payment, "booking": booking})
