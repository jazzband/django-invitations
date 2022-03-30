from django.dispatch import Signal

invite_url_sent = Signal()
invite_accepted = Signal()

"""
@receiver(invite_url_sent, sender=Invitation)
def invite_url_sent(sender, instance, invite_url_sent, inviter, **kwargs):
    pass

@receiver(invite_accepted, sender=Invitation)
def handle_invite_accepted(sender, email, **kwargs):
    pass
"""
