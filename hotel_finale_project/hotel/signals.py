from .models import Reservation
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Reservation)
def Room_available(sender, instance, created, **kwargs):
    """signal for room is available or not"""
    room = instance.room
    if created:
        room.is_available = False
    room.save()

    if instance.check_out_done:
        room.is_available = True

    room.save()
