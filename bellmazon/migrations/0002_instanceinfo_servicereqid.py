# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bellmazon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instanceinfo',
            name='serviceReqId',
            field=models.CharField(default=b'0000', max_length=200),
        ),
    ]
