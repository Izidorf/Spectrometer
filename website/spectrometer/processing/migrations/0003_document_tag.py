# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='tag',
            field=models.CharField(default=datetime.datetime(2015, 3, 5, 20, 56, 8, 871545, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
