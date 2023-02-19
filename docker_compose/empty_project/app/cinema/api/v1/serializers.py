from rest_framework.serializers import ListField, ModelSerializer, SerializerMethodField, CharField

from cinema.models import Filmwork


class FilmWorksSerializer(ModelSerializer):
    type = CharField(source='filmwork_type')

    actors = ListField()
    writers = ListField()
    directors = ListField()

    genres = SerializerMethodField()

    def get_genres(self, filmwork):
        return [genre.name for genre in filmwork.genres.all()]

    class Meta:
        model = Filmwork
        fields = ['id', 'title', 'description', 'creation_date', 'rating', 'type', 'genres', 'actors',
                  'directors', 'writers']
