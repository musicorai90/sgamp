# Generated by Django 2.2.5 on 2020-04-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0016_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='imagen',
            field=models.ImageField(upload_to='pagos/'),
        ),
    ]