# Generated by Django 5.0 on 2024-01-19 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_product_benefits'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='serving_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
