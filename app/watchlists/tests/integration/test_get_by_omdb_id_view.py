import os

import pytest
import requests
from django.urls import reverse


from watchlists.models import Series, Movie, Media


pytestmark = pytest.mark.django_db
BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_get_with_no_query_params(api_client):
    # when
    response = api_client.get(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_type_query_param(api_client):
    # given
    type = "series"
    # when
    response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"type": type})
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_imdb_id_query_param(api_client):
    # given
    imdb_id = "tt13443470"
    # when
    response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id})
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_incorrect_type_query_params(api_client):
    # given
    imdb_id = "tt13443470"
    type = "incorrect_type"
    # when
    response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_incorrect_imdb_id_and_type_query_params(api_client):
    # given
    imdb_id = "incorrect_imdb_id"
    type = "series"
    # when
    response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_post(api_client):
    # when
    response = api_client.post(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_put(api_client):
    # when
    response = api_client.put(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_patch(api_client):
    # when
    response = api_client.patch(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_delete(api_client):
    # when
    response = api_client.delete(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"
