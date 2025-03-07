from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from .models import UserProgression  # Importer UserProgression-modellen
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    email = forms.EmailField(required=True, help_text="En gyldig e-postadresse er påkrevd.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    
    
    def clean_password2(self):
        password = self.cleaned_data.get("password2")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn.")
        
        if not re.search(r'\d', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        return password


def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            # feil melding ved ugyldig innlogg
            messages.error(request, 'Invalid username or password.')
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'register.html', { 'form': form})



@login_required
def profile(request):
    try:
        progression = UserProgression.objects.get(user=request.user)  # Henter brukerens progresjon
    except UserProgression.DoesNotExist:
        progression = None  # Hvis ingen progresjonsdata finnes, settes det til None

    return render(request, 'profile.html', {'progression': progression})

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
