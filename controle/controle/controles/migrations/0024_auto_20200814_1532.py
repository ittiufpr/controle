# Generated by Django 3.0.8 on 2020-08-14 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuns', '0007_auto_20200814_1531'),
        ('controles', '0023_auto_20200814_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucao',
            name='cpf_func',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.Pessoa'),
        ),
    ]
