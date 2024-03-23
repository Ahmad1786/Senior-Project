# Generated by Django 5.0.2 on 2024-03-23 00:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='server',
            name='members',
            field=models.ManyToManyField(related_name='servers', through='servers.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participation',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to='servers.server'),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together={('user', 'server')},
        ),
    ]
