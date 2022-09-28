from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_str

from .app_settings import app_settings
from .utils import import_attribute


# Code credits here to django-allauth
class BaseInvitationsAdapter:
    def stash_verified_email(self, request, email):
        request.session["account_verified_email"] = email

    def unstash_verified_email(self, request):
        ret = request.session.get("account_verified_email")
        request.session["account_verified_email"] = None
        return ret

    def format_email_subject(self, subject, context):
        prefix = app_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site_name = context["site_name"]
            prefix = f"[{site_name}] "
        return prefix + force_str(subject)

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        subject = render_to_string(f"{template_prefix}_subject.txt", context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject, context)

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = f"{template_prefix}_message.{ext}"
                bodies[ext] = render_to_string(template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject,
                bodies["txt"],
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(
                subject,
                bodies["html"],
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def is_open_for_signup(self, request):
        if hasattr(request, "session") and request.session.get(
            "account_verified_email",
        ):
            return True
        elif app_settings.INVITATION_ONLY is True:
            # Site is ONLY open for invites
            return False
        else:
            # Site is open to signup
            return True

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        return email

    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None,
        extra_tags="",
    ):
        """
        Wrapper of `django.contrib.messages.add_message`, that reads
        the message text from a template.
        """
        if "django.contrib.messages" in settings.INSTALLED_APPS:
            try:
                if message_context is None:
                    message_context = {}
                message = render_to_string(message_template, message_context).strip()
                if message:
                    messages.add_message(request, level, message, extra_tags=extra_tags)
            except TemplateDoesNotExist:
                pass


def get_invitations_adapter():
    # Compatibility with legacy allauth only version.
    LEGACY_ALLAUTH = (
        hasattr(settings, "ACCOUNT_ADAPTER")
        and settings.ACCOUNT_ADAPTER == "invitations.models.InvitationsAdapter"
    )
    if LEGACY_ALLAUTH:
        # defer to allauth
        from allauth.account.adapter import get_adapter

        return get_adapter()
    else:
        # load an adapter from elsewhere
        return import_attribute(app_settings.ADAPTER)()
