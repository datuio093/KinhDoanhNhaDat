# Generated by Django 3.2.1 on 2023-05-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_userprofile_is_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='homemypost',
            name='fblink',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
