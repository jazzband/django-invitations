# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_auto_20151126_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
