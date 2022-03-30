# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='e-mail address')),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('key', models.CharField(unique=True, max_length=64, verbose_name='key')),
                ('sent', models.DateTimeField(null=True, verbose_name='sent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
