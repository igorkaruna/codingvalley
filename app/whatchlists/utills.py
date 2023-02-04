import os
from datetime import datetime

import requests

from whatchlists.models import Movie, Series, Season, Episode


def get_omdb_by_search(search: str) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str, session=None):
    if session:
            data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    else:
        data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    return data


def get_season_by_omdbid(series_omdb_id: str, season_numb: int, session) -> dict:
    season = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={series_omdb_id}&Season={season_numb}").json()
    return season


def get_episode_by_omdbid(episode_omdb_id: str, session) -> dict:
    episode = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={episode_omdb_id}").json()
    return episode


def save_movie(imdb_id):
    """Creates movie and return it"""

    movie_data = get_omdb_by_omdbid(imdb_id)

    # extracting only info needed for movie model
    needed_data = {}
    needed_data['title'] = movie_data['Title']

    # converting date format
    released = datetime.strptime(movie_data['Released'], '%d %b %Y').date()
    needed_data['released'] = released

    # editing runtime field
    needed_data['runtime'] = movie_data['Runtime'].split(' ')[0]

    needed_data['genres'] = movie_data['Genre']
    needed_data['poster'] = movie_data['Poster']
    needed_data['imdb_id'] = movie_data['imdbID']
    needed_data['imdb_rating'] = movie_data['imdbRating']

    # initiation of the movie instance and saving
    movie = Movie(**needed_data)
    movie.save()

    return movie


def save_series(imdb_id):
    """At first saves series then iterated through
        season and series and saves them too,
        returns series instance
    """
    session = requests.Session()

    series_data = get_omdb_by_omdbid(imdb_id, session)

    # extracting only info needed for series model
    needed_data = {}
    needed_data['title'] = series_data['Title']
    needed_data['year'] = series_data['Year']

    # converting date format
    released = datetime.strptime(series_data['Released'], '%d %b %Y').date()
    needed_data['released'] = released

    needed_data['genres'] = series_data['Genre']
    needed_data['plot'] = series_data['Plot']
    needed_data['total_seasons'] = series_data['totalSeasons']
    needed_data['poster'] = series_data['Poster']
    needed_data['imdb_id'] = series_data['imdbID']
    needed_data['imdb_rating'] = series_data['imdbRating']

    # initiation of the movie instance and saving
    series = Series(**needed_data)
    series.save()

    # iterationg through seasons
    for season_number in range(1, int(series.total_seasons)+1):
        season_data = get_season_by_omdbid(series.imdb_id, season_number, session)

        # extracting only info needed for season model
        needed_data = {}
        needed_data['season_numb'] = season_data['Season']
        needed_data['total_episodes'] = 0

        season = Season(series=series, **needed_data)

        # iterating through episodes
        episodes = []
        for e in season_data["Episodes"]:
            episode_data = get_episode_by_omdbid(e["imdbID"], session)
            if not episode_data["Response"]:
                break

            # extracting only info needed for series model
            needed_data = {}
            needed_data['title'] = episode_data['Title']

            # converting date format
            released = datetime.strptime(series_data['Released'], '%d %b %Y').date()
            needed_data['released'] = released

            needed_data['episode_numb'] = episode_data['Episode']
            # editing runtime field
            needed_data['runtime'] = episode_data['Runtime'].split(" ")[0]
            needed_data['plot'] = episode_data['Plot']
            needed_data['poster'] = episode_data['Poster']
            imdb_rating = episode_data['imdbRating']

            if imdb_rating not in ["N/A"]:
                needed_data['imdb_rating'] = imdb_rating

            episode = Episode(season=season, **needed_data)
            episodes.append(episode)

        season.total_episodes += len(episodes)
        season.save()
        Episode.objects.bulk_create(episodes)
    return series


def save_to_db_or_get(data: dict):
    '''Function takes data returned by imdb,
       distinguishes wheter it is movie of series,
       than if there is already insctance in db it returns it
       if there is not that calls creation functions
    '''

    # sorting by type (movie or series)
    data_type = data.get('Type', None)

    if data_type == 'movie':
        # checking for existing movie
        try:
            movie = Movie.objects.get(imdb_id=data["imdbID"])
        except Movie.DoesNotExist:
            movie = save_movie(data), "movie"

        return movie
    elif data_type == 'series':
        try:
            series = Series.objects.get(imdb_id=data["imdbID"])
        except Series.DoesNotExist:
            series = save_series(data)

        return series, "series"
