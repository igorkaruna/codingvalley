import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestDiscussionViewSet:
    # LIST
    def test_list_with_unauthenticated_user_with_no_discussions(self, api_client):
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 0, "The response must contain no discussions"

    def test_list_with_unauthenticated_user(self, api_client):
        # GIVEN
        baker.make("discussions.Discussion")
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 1, "The response must contain one discussion"

    def test_list_with_authenticated_user(self, api_client, user):
        # GIVEN
        baker.make("discussions.Discussion")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 1, "The response must contain one discussion"

    # RETRIEVE
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # GIVEN
        discussion = baker.make("discussions.Discussion")
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('id') == str(discussion.id),  "The response must contain id of the given discussion"

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # GIVEN
        discussion = baker.make("discussions.Discussion")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('id') == str(discussion.id),  "The response must contain id of the given discussion"

    # CREATE
    def test_create_with_unauthenticated_user(self, api_client):
        # GIVEN
        discussion = {'title': 'some title', 'content': 'some content'}
        # WHEN
        post_response = api_client.post(reverse("discussions_app:discussions-list"), discussion)
        get_response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert post_response.status_code == 401, "Status code of response must be 401"
        assert len(get_response.json()) == 0, "The response must contain no discussions"
