# Generated by Django 3.2.1 on 2023-05-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='star',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
