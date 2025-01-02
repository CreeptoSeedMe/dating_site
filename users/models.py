# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    looking_for = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    interests = models.ManyToManyField('Interest')
    last_active = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(default=False)
    max_distance = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    age_min_preference = models.IntegerField(
        default=18,
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    age_max_preference = models.IntegerField(
        default=100,
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    @property
    def is_online(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.last_active >= timezone.now() - timedelta(minutes=5)

    def get_primary_photo(self):
        return self.photos.filter(is_primary=True).first() or self.photos.first()

    def get_matches(self):
        return Match.objects.filter(models.Q(user1=self) | models.Q(user2=self))

    def get_likes_received(self):
        return Like.objects.filter(liked_profile=self)

    def get_likes_given(self):
        return Like.objects.filter(liker=self)

    def __str__(self):
        return f"{self.user.username}'s profile"


class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_photos/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other photos to non-primary
            self.profile.photos.exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)


class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
