from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from whatchlists.models import Movie, Series
from whatchlists.serializers import MovieSerializer, SeriesSerializer, SeasonSerializer
from whatchlists.services import db_saving, omdb_requests


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


@api_view()
def search_by_search_view(request):
    search = request.query_params['search']
    search_results = omdb_requests.get_omdb_by_search(search)
    return Response(search_results)


class GetByOmdbIdView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        type = self.request.query_params["type"]
        imdb_id = self.request.query_params["imdb_id"]
        if type == "movie":
            try:
                movie = Movie.objects.get(imdb_id=imdb_id)
            except Movie.DoesNotExist:
                movie = db_saving.save_movie(imdb_id)
            return movie
        elif type == "series":
            try:
                series = Series.objects.get(imdb_id=imdb_id)
            except Series.DoesNotExist:
                series = db_saving.save_series(imdb_id)
            return series

    def get_serializer_class(self):
        type = self.request.query_params["type"]
        if type == "movie":
            return MovieSerializer
        elif type == "series":
            return SeriesSerializer

    def get_serializer_context(self):
        context = {}
        context["imdb_rating"] = self.request.query_params.get("imdb_rating", None)
        return context


class GetSeason(RetrieveAPIView):
    serializer_class = SeasonSerializer

    def get_object(self):
        imdb_id = self.request.query_params["imdb_id"]
        season_number = self.request.query_params["season"]
        series = Series.objects.get(imdb_id=imdb_id)
        season = series.seasons.get(season_numb=season_number)
        return season

    def get_serializer_context(self):
        context = {}
        context["imdb_rating"] = self.request.query_params.get("imdb_rating", None)
        return context
