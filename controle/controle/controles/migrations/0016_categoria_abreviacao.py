# Generated by Django 3.0.8 on 2020-08-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0015_auto_20200805_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='abreviacao',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]
