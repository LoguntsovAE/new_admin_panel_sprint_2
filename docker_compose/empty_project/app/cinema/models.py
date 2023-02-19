import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, default=str())

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkType(models.TextChoices):
        FRESHMAN = 'movie', _('Movie')
        SOPHOMORE = 'tv_show', _('TV show')

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    title = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, default=str())
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    filmwork_type = models.CharField(_('type'), choices=FilmworkType.choices, max_length=255)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    rating = models.FloatField(
        _('rating'), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')


class PersonFilmwork(UUIDMixin):
    class RolesTypes(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), blank=True, choices=RolesTypes.choices, default=str())
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = (
            ('film_work', 'person', 'role')
        )


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('genre'))
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        unique_together = (
            ('film_work', 'genre')
        )
