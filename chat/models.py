from django.db import models
from django.db.models import Q
from matching.models import Match

class Conversation(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)

    def get_messages(self):
        return self.messages.all().order_by('timestamp')

    def get_other_user(self, profile):
        return self.match.get_other_user(profile)

    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()

    def __str__(self):
        return f"Conversation between {self.match.user1.user.username} and {self.match.user2.user.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey('users.Profile', related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.user.username} at {self.timestamp}"

    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

class MessageReaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', '👍'),
        ('LOVE', '❤️'),
        ('LAUGH', '😄'),
        ('SURPRISED', '😮'),
        ('SAD', '😢'),
        ('ANGRY', '😠')
    ]

    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.Profile', related_name='message_reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user.user.username} reacted with {self.get_reaction_display()} to message"