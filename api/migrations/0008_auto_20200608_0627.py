# Generated by Django 3.0.7 on 2020-06-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200608_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=120, unique=True),
        ),
    ]
