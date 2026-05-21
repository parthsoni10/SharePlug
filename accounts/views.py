import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Map.models import EVStation, StationRegistration, Booking, CheckIn, Bookmark


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST.get("Username", "").strip()
        password = request.POST.get("password", "")
        if not User.objects.filter(username=username).exists():
            messages.error(request, "No account found with that username.")
            return redirect('/login/')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect password.")
            return redirect('/login/')
        login(request, user)
        messages.success(request, f"Welcome back, {user.first_name or user.username}! ⚡")
        return redirect('/')
    return render(request, "login.html", {"page": "Login – SharePlug"})

def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        first_name = request.POST.get("firstname", "").strip()
        last_name = request.POST.get("lastname", "").strip()
        username = request.POST.get("Username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('/register/')
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('/register/')
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
            messages.error(request, "Username must start with a letter and contain only letters, numbers, underscores.")
            return redirect('/register/')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/register/')
        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created! Please log in. ✅")
        return redirect('/login/')
    return render(request, "register.html", {"page": "Sign Up – SharePlug"})

def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/login/')

@login_required
def profile_page(request):
    user = request.user
    business_profile = getattr(user, 'business_profile', None)
    stats = {
        'checkins': CheckIn.objects.filter(user=user).count(),
        'bookmarks': Bookmark.objects.filter(user=user).count(),
        'bookings': Booking.objects.filter(user=user).count(),
        'registrations': StationRegistration.objects.filter(owner=user).count(),
        'stations': EVStation.objects.filter(owner=user).count(),
    }
    return render(request, 'profile.html', {
        'page': 'My Profile – SharePlug',
        'business_profile': business_profile,
        'stats': stats,
    })
