# Generated by Django 4.1.6 on 2023-03-16 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ejercicio1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pasos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_paso', models.CharField(max_length=150)),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejercicio1.plato')),
            ],
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejercicio1.plato')),
            ],
        ),
    ]
