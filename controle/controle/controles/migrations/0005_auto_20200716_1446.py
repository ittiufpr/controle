# Generated by Django 2.2.2 on 2020-07-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0004_auto_20200415_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
