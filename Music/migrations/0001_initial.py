# Generated by Django 2.2.6 on 2019-12-06 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=250)),
                ('album_title', models.CharField(max_length=250)),
                ('album_genre', models.CharField(max_length=100)),
                ('album_logo', models.CharField(max_length=1000)),
                ('album_year', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=250)),
                ('song_genre', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
                ('albums', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Music.Album')),
            ],
        ),
    ]
