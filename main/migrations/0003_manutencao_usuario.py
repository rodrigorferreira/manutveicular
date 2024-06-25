# Generated by Django 5.0.6 on 2024-06-13 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customuser_cnpj_customuser_cpf_customuser_is_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='manutencao',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
