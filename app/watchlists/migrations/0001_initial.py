# Generated by Django 4.1.5 on 2023-02-07 22:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('released', models.DateField(verbose_name='Release date')),
                ('genres', models.CharField(max_length=255)),
                ('poster', models.URLField()),
                ('plot', models.TextField()),
                ('imdb_id', models.CharField(max_length=50)),
                ('imdb_rating', models.FloatField()),
                ('media_type', models.CharField(choices=[('MOVIE', 'Movie'), ('SERIES', 'Series')], max_length=6)),
                ('runtime', models.PositiveIntegerField(blank=True, null=True)),
                ('total_seasons', models.PositiveIntegerField(blank=True, null=True)),
                ('year', models.CharField(blank=True, help_text='Use such format: 2018-2022', max_length=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('season_numb', models.PositiveIntegerField()),
                ('total_episodes', models.PositiveIntegerField()),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='watchlists.media')),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
                'ordering': ['season_numb'],
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('released', models.DateField()),
                ('episode_numb', models.PositiveIntegerField()),
                ('runtime', models.PositiveIntegerField()),
                ('plot', models.TextField()),
                ('poster', models.URLField()),
                ('imdb_rating', models.FloatField(blank=True, null=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='watchlists.season')),
            ],
            options={
                'verbose_name': 'Episode',
                'verbose_name_plural': 'Episodes',
                'ordering': ['episode_numb'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('watchlists.media',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('watchlists.media',),
        ),
    ]