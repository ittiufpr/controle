# Generated by Django 3.0.8 on 2020-08-14 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuns', '0004_auto_20200814_1345'),
        ('controles', '0020_devolucao_laudo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucao',
            name='cpf_func',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.Funcionario'),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='cpf_func',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emprestimo_cpf_funcionario', to='comuns.Funcionario'),
        ),
    ]
