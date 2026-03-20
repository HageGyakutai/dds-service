from django.urls import reverse


def test_admin_index_redirects_to_login(client):
    response = client.get(reverse("admin:index"))
    assert response.status_code == 302
