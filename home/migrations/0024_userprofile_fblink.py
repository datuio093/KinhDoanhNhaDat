# Generated by Django 3.2.1 on 2023-05-30 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_remove_homemypost_fblink'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='fblink',
            field=models.TextField(blank=True, null=True),
        ),
    ]
