from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Distributor


@receiver(pre_save, sender=Distributor)
def capture_previous_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return
    previous = sender.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    instance._previous_status = previous


@receiver(post_save, sender=Distributor)
def send_approval_email(sender, instance, created, **kwargs):
    previous_status = getattr(instance, '_previous_status', None)
    if created:
        return
    if instance.status == Distributor.Status.APPROVED and previous_status != Distributor.Status.APPROVED:
        send_mail(
            subject='Your MHD distributor account has been approved',
            message=(
                f'Hello {instance.contact_person},\n\n'
                'Your distributor account has been approved. You can now access the B2B portal and place orders.\n\n'
                'Regards,\nMHD Team'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=True,
        )