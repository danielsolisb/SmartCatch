# Generated by Django 4.2.4 on 2024-08-06 00:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Estación')),
                ('address', models.CharField(max_length=50, null=True)),
                ('telephone', models.IntegerField()),
                ('coordinates', models.CharField(max_length=100, null=True)),
                ('user_ID', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]