# Generated by Django 3.2.1 on 2023-05-27 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20230527_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='homemypost',
            name='listimages',
            field=models.ManyToManyField(blank=True, to='home.ListImage'),
        ),
        migrations.RemoveField(
            model_name='homemypost',
            name='images',
        ),
        migrations.AddField(
            model_name='homemypost',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
