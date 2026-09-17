from django import forms
from django.contrib.auth.models import User
from .models import Profile, Booking, Review, BarberProfile, PortfolioVideo

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    role=forms.ChoiceField(choices=Profile.ROLE)
    class Meta:
        model=User
        fields=("first_name","last_name","username","email","password")
    def save(self,commit=True):
        user=super().save(commit=False); user.set_password(self.cleaned_data["password"])
        if commit:
            user.save(); Profile.objects.create(user=user,role=self.cleaned_data["role"])
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking; fields=("date","time","note")
        widgets={"date":forms.DateInput(attrs={"type":"date"}),"time":forms.TimeInput(attrs={"type":"time"})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review; fields=("rating","text")
        widgets={"rating":forms.Select(choices=[(i,i) for i in range(5,0,-1)])}


class BarberProfileForm(forms.ModelForm):
    class Meta:
        model = BarberProfile
        fields = ["bio", "region", "city", "address", "phone", "experience", "working_hours",
                  "cover", "latitude", "longitude", "instagram", "telegram"]

class PortfolioVideoForm(forms.ModelForm):
    class Meta:
        model = PortfolioVideo
        fields = ["video", "title"]
