# Generated by Django 3.2 on 2023-12-17 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_reviewproduct_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewproduct',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 17, 15, 6, 2, 579593)),
        ),
    ]
