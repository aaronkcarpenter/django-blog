# Generated by Django 4.0.5 on 2022-10-26 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='publish'),
        ),
    ]
