# Generated by Django 3.2.7 on 2022-11-13 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20221112_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='School type'),
        ),
    ]
