# Generated by Django 4.2.11 on 2024-04-24 21:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_chore_assignees_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='num_payers_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill',
            name='payers_paid',
            field=models.ManyToManyField(blank=True, related_name='payers_paid', to=settings.AUTH_USER_MODEL),
        ),
    ]
