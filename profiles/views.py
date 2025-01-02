# profiles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, ProfilePhoto
from .forms import ProfileForm, ProfilePhotoForm

@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(Profile, user__username=username)
        is_own_profile = request.user.profile == profile
    else:
        profile = request.user.profile
        is_own_profile = True

    context = {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'photos': profile.photos.all(),
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def add_photo(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = request.user.profile
            photo.save()
            messages.success(request, 'Photo added successfully!')
            return redirect('profile')
    else:
        form = ProfilePhotoForm()

    return render(request, 'profiles/add_photo.html', {'form': form})