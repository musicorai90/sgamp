# Generated by Django 2.2.5 on 2020-05-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0019_partituramusico_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='apellido',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='telefono',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]