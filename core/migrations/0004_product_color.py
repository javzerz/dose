# Generated by Django 5.0 on 2024-01-16 01:43

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
    ]