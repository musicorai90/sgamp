# Generated by Django 2.2.5 on 2020-03-10 17:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='musico',
            name='fecha_ing',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
