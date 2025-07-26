from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Can be extended with additional fields as needed.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Model to represent a conversation between multiple users.
    Tracks which users are involved in a conversation.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participant_names = ', '.join([user.username for user in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participant_names += f' and {self.participants.count() - 3} others'
        return f"Conversation: {participant_names}"

    @property
    def last_message(self):
        """Get the most recent message in this conversation"""
        return self.messages.first()


class Message(models.Model):
    """
    Model to represent individual messages within conversations.
    Contains sender, conversation, and message content.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent this message"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Conversation this message belongs to"
    )
    content = models.TextField(help_text="Message content")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}{'...' if len(self.content) > 50 else ''}"

    def save(self, *args, **kwargs):
        """Update conversation's updated_at when a new message is added"""
        super().save(*args, **kwargs)
        self.conversation.save()  # This will update the updated_at field
