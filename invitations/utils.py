from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.utils import six

from .app_settings import app_settings

try:
    import importlib
except:
    from django.utils import importlib


def import_attribute(path):
    assert isinstance(path, six.string_types)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def get_invitation_model():
    """
    Returns the Invitation model that is active in this project.
    """
    path = app_settings.INVITATION_MODEL
    try:
        return django_apps.get_model(path)
    except ValueError:
        raise ImproperlyConfigured(
            "path must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "path refers to model '%s' that\
             has not been installed" % app_settings.INVITATION_MODEL
        )
