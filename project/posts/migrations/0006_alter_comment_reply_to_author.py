# Generated by Django 5.0.2 on 2024-04-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_rename_reply_to_auth_comment_reply_to_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to_author',
            field=models.CharField(default='Temp', max_length=30),
            preserve_default=False,
        ),
    ]