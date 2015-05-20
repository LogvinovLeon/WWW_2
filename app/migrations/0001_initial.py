# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(max_length=100, null=True)),
                ('name', models.TextField(max_length=100)),
                ('blanks_received', models.IntegerField(default=0)),
                ('can_vote', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Constituencies',
            },
        ),
        migrations.CreateModel(
            name='Gmina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(max_length=100, null=True)),
                ('name', models.TextField(max_length=100)),
                ('version', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Gminas',
            },
        ),
        migrations.CreateModel(
            name='Powiat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(max_length=100, null=True)),
                ('name', models.TextField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Powiats',
            },
        ),
        migrations.CreateModel(
            name='Voivodeship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(max_length=100, null=True)),
                ('name', models.TextField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Voivodeships',
            },
        ),
        migrations.AddField(
            model_name='powiat',
            name='voivodeship',
            field=models.ForeignKey(to='app.Voivodeship'),
        ),
        migrations.AddField(
            model_name='gmina',
            name='powiat',
            field=models.ForeignKey(to='app.Powiat'),
        ),
        migrations.AddField(
            model_name='constituency',
            name='gmina',
            field=models.ForeignKey(to='app.Gmina'),
        ),
    ]
