# Generated by Django 4.2.4 on 2025-01-14 02:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Station', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='user_ID',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
