# Generated by Django 4.2 on 2023-05-06 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payment_ststus',
            field=models.BooleanField(default=False),
        ),
    ]
