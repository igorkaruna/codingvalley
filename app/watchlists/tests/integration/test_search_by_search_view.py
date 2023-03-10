import os

import requests
from django.urls import reverse


BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_get_with_no_query_params(api_client):
    # when
    response = api_client.get(reverse("watchlists_app:search"))
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_search_query_param(api_client):
    # given
    search = "Game of Thrones"
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}")
    # when
    response = api_client.get(reverse("watchlists_app:search"), {"search": search})
    # then
    assert response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert response.status_code == 200, "Status code of response must be 200"


def test_get_with_search_and_year_query_params(api_client):
    # given
    search = "Game of Thrones"
    year = 2016
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}")
    # when
    response = api_client.get(reverse("watchlists_app:search"), {"search": search, "year": year})
    # then
    assert response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert response.status_code == 200, "Status code of response must be 200"


def test_get_with_search_and_page_query_params(api_client):
    # given
    search = "Game of Thrones"
    page = 4
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&page={page}")
    # when
    response = api_client.get(reverse("watchlists_app:search"), {"search": search, "page": page})
    # then
    assert response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert response.status_code == 200, "Status code of response must be 200"


def test_get_with_year_and_page_query_params(api_client):
    # given
    year = 2016
    page = 4
    # when
    response = api_client.get(reverse("watchlists_app:search"), {"year": year, "page": page})
    # then
    assert response.status_code == 404, "Status code of response must be 404"


def test_get_with_search_and_year_and_page_query_params(api_client):
    # given
    search = "Game"
    year = 2016
    page = 4
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}&page={page}")
    # when
    response = api_client.get(reverse("watchlists_app:search"), {"search": search, "year": year, "page": page})
    # then
    assert response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert response.status_code == 200, "Status code of response must be 200"


def test_post(api_client):
    # when
    response = api_client.post(reverse("watchlists_app:search"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_put(api_client):
    # when
    response = api_client.put(reverse("watchlists_app:search"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_patch(api_client):
    # when
    response = api_client.patch(reverse("watchlists_app:search"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"


def test_delete(api_client):
    # when
    response = api_client.delete(reverse("watchlists_app:search"))
    # then
    assert response.status_code == 405, "Status code of response must be 405"
