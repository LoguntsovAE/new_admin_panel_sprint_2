import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(('CREATE SCHEMA content;',)),
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation date')),
                ('filmwork_type', models.CharField(choices=[('movie', 'Movie'), ('tv_show', 'TV show')], max_length=255, verbose_name='type')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='file')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
            ],
            options={
                'verbose_name': 'film',
                'verbose_name_plural': 'films',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('full_name', models.CharField(max_length=255, verbose_name='full_name')),
            ],
            options={
                'verbose_name': 'actor',
                'verbose_name_plural': 'actors',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('role', models.TextField(blank=True, choices=[('actor', 'actor'), ('director', 'director'), ('writer', 'writer')], default='', verbose_name='role')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.person')),
            ],
            options={
                'db_table': 'content"."person_film_work',
                'unique_together': {('film_work', 'person', 'role')},
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.genre', verbose_name='genre')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre_film_work',
                'unique_together': {('film_work', 'genre')},
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='cinema.GenreFilmwork', to='cinema.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='cinema.PersonFilmwork', to='cinema.person'),
        ),
    ]
