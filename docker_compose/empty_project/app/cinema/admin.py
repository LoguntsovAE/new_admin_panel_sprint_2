from django.contrib import admin
from django.contrib.admin.decorators import display

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'id')
    list_display = ('name', 'created_at', 'updated_at')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    fields = ('person',)
    autocomplete_fields = ('person', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_filter = ('filmwork_type', 'genres__name')
    list_prefetch_related = ('persons', 'genres')
    search_fields = ('title', 'description', 'id')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'filmwork_type', 'creation_date', 'rating', 'created_at', 'updated_at', 'get_genres')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.list_prefetch_related)

    @display(description='Жанры фильма')
    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    search_fields = ('full_name', 'id')
    list_display = ('full_name', 'created_at', 'updated_at')
