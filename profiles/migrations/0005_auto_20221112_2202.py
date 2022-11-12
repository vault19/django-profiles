# Generated by Django 3.2.7 on 2022-11-12 21:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20221014_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='edu_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='EDUID'),
        ),
        migrations.AddField(
            model_name='school',
            name='number_of_students',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of Students'),
        ),
        migrations.AddField(
            model_name='school',
            name='timestamp_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 10, 10, 10, 10), verbose_name='Added'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='timestamp_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='replaced_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='profiles.membership', verbose_name='Replaced by'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='profiles.school'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='profiles.address'),
        ),
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='profiles.address'),
        ),
        migrations.AlterField(
            model_name='school',
            name='ineko_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='INEKO ID'),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='KODSKO'),
        ),
    ]
