# Generated by Django 4.1.5 on 2023-02-03 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatchlists', '0008_remove_movie_genres_remove_series_genres_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ['episode_numb'], 'verbose_name': 'Episode', 'verbose_name_plural': 'Episodes'},
        ),
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ['season_numb'], 'verbose_name': 'Season', 'verbose_name_plural': 'Seasons'},
        ),
        migrations.AddField(
            model_name='episode',
            name='imdb_rating',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='imdb_rating',
            field=models.FloatField(default=1.0),
            preserve_default=False,
        ),
    ]
