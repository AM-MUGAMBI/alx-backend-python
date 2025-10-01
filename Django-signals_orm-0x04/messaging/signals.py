from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, nothing to compare

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Only log if the content has changed
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Ensures all related messages, notifications, and histories are cleaned up
    when a user is deleted. Mostly redundant if using CASCADE, but included
    for completeness and project requirements.
    """
    # Delete notifications directly linked to user (just in case)
    Notification.objects.filter(user=instance).delete()

    # If you want to double-clean, also check for messages:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Since histories are linked to messages, they will be auto-deleted
