from django.dispatch import Signal

invite_url_sent = Signal(providing_args=['invite_url_sent', 'inviter'])
invite_accepted = Signal(providing_args=['email'])

"""
@receiver(invite_url_sent, sender=Invitation)
def invite_url_sent(sender, instance, invite_url_sent, inviter, **kwargs):
    pass

@receiver(invite_accepted, sender=Invitation)
def handle_invite_accepted(sender, email, **kwargs):
    pass
"""
