# Generated by Django 3.0.4 on 2020-05-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
