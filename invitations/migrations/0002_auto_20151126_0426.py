# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

EMAIL_MAX_LENGTH = getattr(settings, 'INVITATIONS_EMAIL_MAX_LENGTH', 254)



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(unique=True, max_length=EMAIL_MAX_LENGTH, verbose_name='e-mail address'),
        ),
    ]
