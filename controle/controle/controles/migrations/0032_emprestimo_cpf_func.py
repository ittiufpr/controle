# Generated by Django 3.0.8 on 2020-08-14 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuns', '0009_auto_20200814_1706'),
        ('controles', '0031_auto_20200814_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='cpf_func',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='emprestimo_cpf_funcionario', to='comuns.Pessoa'),
            preserve_default=False,
        ),
    ]