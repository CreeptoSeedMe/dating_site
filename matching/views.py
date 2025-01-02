from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Like, Match
from users.models import Profile
from .forms import SearchFiltersForm

@login_required
def browse_profiles(request):
    profiles = Profile.objects.exclude(user=request.user)
    filters_form = SearchFiltersForm(request.GET)
    if filters_form.is_valid():
        age_min = filters_form.cleaned_data.get('age_min')
        age_max = filters_form.cleaned_data.get('age_max')
        gender = filters_form.cleaned_data.get('gender')
        location = filters_form.cleaned_data.get('location')

        if age_min:
            profiles = profiles.filter(birth_date__year__lte=(date.today().year - age_min))
        if age_max:
            profiles = profiles.filter(birth_date__year__gte=(date.today().year - age_max))
        if gender:
            profiles = profiles.filter(gender=gender)
        if location:
            profiles = profiles.filter(location__icontains=location)

    return render(request, 'matching/browse.html', {'profiles': profiles, 'filters_form': filters_form})

@login_required
def like_profile(request, profile_id):
    liked_profile = get_object_or_404(Profile, id=profile_id)
    like, created = Like.objects.get_or_create(liker=request.user.profile, liked_profile=liked_profile)
    if created:
        messages.success(request, f'You liked {liked_profile.user.username}!')
    else:
        messages.info(request, f'You already liked {liked_profile.user.username}.')
    return redirect('browse_profiles')

@login_required
def matches(request):
    matches = Match.objects.filter(Q(user1=request.user.profile) | Q(user2=request.user.profile))
    return render(request, 'matching/matches.html', {'matches': matches})