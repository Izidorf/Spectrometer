# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0003_document_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='source',
            field=models.ImageField(default=datetime.datetime(2015, 3, 15, 9, 45, 19, 629530, tzinfo=utc), upload_to=b'images'),
            preserve_default=False,
        ),
    ]
