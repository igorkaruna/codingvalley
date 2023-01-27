# Generated by Django 4.1.5 on 2023-01-27 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_liked', to='reviews.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ReviewLikes',
                'verbose_name_plural': 'ReviewLikes',
            },
        ),
    ]
