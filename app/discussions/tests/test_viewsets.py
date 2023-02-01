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