# Generated by Django 2.2.5 on 2020-06-06 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0021_auto_20200605_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
    ]