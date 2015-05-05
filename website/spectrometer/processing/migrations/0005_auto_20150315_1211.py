# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0004_document_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='docfile',
        ),
        migrations.AlterField(
            model_name='document',
            name='source',
            field=models.ImageField(upload_to=b'documents/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
