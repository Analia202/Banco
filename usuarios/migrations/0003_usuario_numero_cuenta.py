# Generated by Django 5.2 on 2025-05-06 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_ci'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='numero_cuenta',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
