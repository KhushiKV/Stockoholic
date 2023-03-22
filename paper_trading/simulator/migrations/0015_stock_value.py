# Generated by Django 4.1.6 on 2023-03-22 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0014_remove_stock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]