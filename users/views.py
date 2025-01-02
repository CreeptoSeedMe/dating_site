from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, ProfilePhotoForm
from .models import Profile, ProfilePhoto

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('profile')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profiles/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def add_photo(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = request.user.profile
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('profile')
    else:
        form = ProfilePhotoForm()
    return render(request, 'profiles/add_photo.html', {'form': form})