from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile

class Like(models.Model):
    liker = models.ForeignKey(Profile, related_name='likes_given', on_delete=models.CASCADE)
    liked_profile = models.ForeignKey(Profile, related_name='likes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_super_like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('liker', 'liked_profile')

    def __str__(self):
        return f"{self.liker.user.username} likes {self.liked_profile.user.username}"

class Match(models.Model):
    user1 = models.ForeignKey(Profile, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='matches_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match between {self.user1.user.username} and {self.user2.user.username}"

    def get_other_user(self, profile):
        return self.user2 if self.user1 == profile else self.user1

@receiver(post_save, sender=Like)
def check_for_match(sender, instance, created, **kwargs):
    if created:
        # Check if there's a mutual like
        mutual_like = Like.objects.filter(
            liker=instance.liked_profile,
            liked_profile=instance.liker
        ).exists()

        if mutual_like:
            # Create a match
            Match.objects.get_or_create(
                user1=instance.liker,
                user2=instance.liked_profile
            )

class Block(models.Model):
    blocker = models.ForeignKey(Profile, related_name='blocks_given', on_delete=models.CASCADE)
    blocked_profile = models.ForeignKey(Profile, related_name='blocks_received', on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked_profile')

    def __str__(self):
        return f"{self.blocker.user.username} blocked {self.blocked_profile.user.username}"

class Report(models.Model):
    REPORT_REASONS = [
        ('FAKE', 'Fake Profile'),
        ('SPAM', 'Spam'),
        ('OFFENSIVE', 'Offensive Content'),
        ('HARASSMENT', 'Harassment'),
        ('OTHER', 'Other')
    ]

    reporter = models.ForeignKey(Profile, related_name='reports_made', on_delete=models.CASCADE)
    reported_profile = models.ForeignKey(Profile, related_name='reports_received', on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Report by {self.reporter.user.username} against {self.reported_profile.user.username}"