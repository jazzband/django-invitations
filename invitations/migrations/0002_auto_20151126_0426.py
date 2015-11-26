# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='e-mail address'),
        ),
    ]
