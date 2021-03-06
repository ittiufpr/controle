# Generated by Django 3.0.8 on 2020-08-14 17:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comuns', '0004_auto_20200814_1345'),
        ('controles', '0019_emprestimo_cpf_func'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laudo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=200)),
                ('documento', models.FileField(upload_to='uploads/laudo/')),
                ('cpf_func', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.Pessoa')),
                ('id_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controles.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Devolucao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_devolucao', models.DateField(default=django.utils.timezone.now)),
                ('cpf_func', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuns.Pessoa')),
                ('emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controles.Emprestimo')),
                ('laudo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controles.Laudo')),
            ],
        ),
    ]
