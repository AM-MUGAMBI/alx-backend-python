import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    # Override the default id with UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    # Use AbstractUser's first_name and last_name fields (non-null enforced via blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    # Email as unique, required, override AbstractUser's email field
    email = models.EmailField(unique=True, blank=False)

    # Password hash handled by AbstractUser's password field (usually hashed)
    # But to follow spec, alias password_hash to password (not recommended but for schema matching)
    # You can just rely on `password` field in AbstractUser, but if needed:
    password_hash = models.CharField(max_length=128, blank=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Role enum
    GUEST = 'guest'
    HOST = 'host'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (GUEST, 'Guest'),
        (HOST, 'Host'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=GUEST)

    created_at = models.DateTimeField(default=timezone.now)

    # Override username field to email for authentication (optional)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        # keep password_hash and password in sync (optional, not recommended)
        if self.password and self.password != self.password_hash:
            self.password_hash = self.password
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    message_body = models.TextField(blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} at {self.sent_at}"

