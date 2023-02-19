from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cinema.models import Filmwork, PersonFilmwork

from .serializers import FilmWorksSerializer


class CinemaGenericViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = []
    http_method_names = ['get']
    serializer_class = FilmWorksSerializer

    @staticmethod
    def _annotate_persons(role):
        return ArrayAgg('persons__full_name', filter=Q(personfilmwork__role__icontains=role), distinct=True)

    def get_queryset(self):
        qs = Filmwork.objects.all().prefetch_related('genres', 'persons').annotate(
            actors=self._annotate_persons(PersonFilmwork.RolesTypes.ACTOR),
            writers=self._annotate_persons(PersonFilmwork.RolesTypes.WRITER),
            directors=self._annotate_persons(PersonFilmwork.RolesTypes.DIRECTOR)
        )
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
