# Generated by Django 4.2.7 on 2023-11-22 17:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0011_auto_20230920_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookresponse',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
