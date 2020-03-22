# Generated by Django 2.2.5 on 2020-03-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0004_auto_20200310_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='galeria/')),
                ('descripcion', models.TextField()),
                ('fecha', models.DateField()),
                ('visible', models.CharField(choices=[('S', 'Si'), ('N', 'No')], max_length=1)),
            ],
        ),
    ]