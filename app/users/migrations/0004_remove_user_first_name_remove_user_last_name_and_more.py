<<<<<<< HEAD
# Generated by Django 4.1.5 on 2023-01-31 16:28
=======
# Generated by Django 4.1.5 on 2023-01-31 16:58
>>>>>>> bf8e8ae (users-makemigrations)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatchlists', '0007_rename_episode_num_episode_episode_numb_and_more'),
        ('users', '0003_user_favourite_movies_user_favourite_series'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_movies',
<<<<<<< HEAD
            field=models.ManyToManyField(related_name='users', to='whatchlists.movie'),
=======
            field=models.ManyToManyField(blank=True, related_name='users', to='whatchlists.movie'),
>>>>>>> bf8e8ae (users-makemigrations)
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_series',
<<<<<<< HEAD
            field=models.ManyToManyField(related_name='users', to='whatchlists.series'),
=======
            field=models.ManyToManyField(blank=True, related_name='users', to='whatchlists.series'),
>>>>>>> bf8e8ae (users-makemigrations)
        ),
    ]