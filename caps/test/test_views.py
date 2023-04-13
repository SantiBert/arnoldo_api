import pytest

from rest_framework.test import APIClient

from caps.models import Season, Episodies

from django.urls import reverse

from users.test.fixtures import common_user_token

@pytest.mark.django_db()
def test_get_season_list_successfully():
    client = APIClient()
    season = Season.objects.create(name="Temaporada 1")
    season2 = Season.objects.create(name="Temaporada 2")
    url = reverse("seasons")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json().get("seasons")
    assert len(data) == 2
    
@pytest.mark.django_db()
def test_get_season_successfully():
    client = APIClient()
    name = "Temaporada 1"
    season = Season.objects.create(name="Temaporada 1")
    url = reverse("season-detail", kwargs={"season_id": season.id})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json().get("data")
    assert data.get("name") == name
    
@pytest.mark.django_db()
def test_get_season_wrong_id():
    client = APIClient()
    name = "Temaporada 1"
    url = reverse("season-detail", kwargs={"season_id": 999})
    response = client.get(url)
    assert response.status_code == 404
    data = response.json().get("error")
    assert data == "Seasons does not exist"

@pytest.mark.django_db()
def test_create_season_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    payload = {
        "name": "Temporada 1",
        "image": "http://elarnoldo.pythonanywhere.com/media/Season/Sin_t%C3%ADtulo-1_LvZBxJQ.png",
        "banner": "https://elarnoldo.pythonanywhere.com/media/Season/port1_Mesa_de_trabajo_1.png",
        "description": "La segunda temporada de Hey Arnold! fue emitida entre el 22 de septiembre de 1997 y el 1 de diciembre del mismo año."
        }
    
    url = reverse("season-create")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    
@pytest.mark.django_db()
def test_create_season_bad_request(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    payload = {
        "name": False,
        "image": "http://elarnoldo.pythonanywhere.com/media/Season/Sin_t%C3%ADtulo-1_LvZBxJQ.png",
        "banner": "https://elarnoldo.pythonanywhere.com/media/Season/port1_Mesa_de_trabajo_1.png",
        "description": "La segunda temporada de Hey Arnold! fue emitida entre el 22 de septiembre de 1997 y el 1 de diciembre del mismo año."
        }
    
    url = reverse("season-create")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 400
    
@pytest.mark.django_db()
def test_update_season_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    payload = {
        "name":"Temporada b",
        "image": "http://elarnoldo.pythonanywhere.com/media/Season/Sin_t%C3%ADtulo-1_LvZBxJQ.png",
        "banner": "https://elarnoldo.pythonanywhere.com/media/Season/port1_Mesa_de_trabajo_1.png",
        "description": "La segunda temporada de Hey Arnold! fue emitida entre el 22 de septiembre de 1997 y el 1 de diciembre del mismo año."
        }
    url = reverse("season-edit", kwargs={"season_id": season.id})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    
@pytest.mark.django_db()
def test_update_season_dont_exists(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    payload = {
        "name":"Temporada b",
        "image": "http://elarnoldo.pythonanywhere.com/media/Season/Sin_t%C3%ADtulo-1_LvZBxJQ.png",
        "banner": "https://elarnoldo.pythonanywhere.com/media/Season/port1_Mesa_de_trabajo_1.png",
        "description": "La segunda temporada de Hey Arnold! fue emitida entre el 22 de septiembre de 1997 y el 1 de diciembre del mismo año."
        }
    url = reverse("season-edit", kwargs={"season_id": 9999})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 404
    data = response.json().get("error")
    assert data == "Season does not exist"

@pytest.mark.django_db()
def test_delete_season_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")

    url = reverse("season-delete", kwargs={"season_id": season.id})
    response = client.delete(
        url
    )
    assert response.status_code == 200
    data = response.json().get("message")
    assert data == "Season deleted"
    
    url = reverse("season-detail", kwargs={"season_id": season.id})
    response = client.get(url)
    assert response.status_code == 404
    
@pytest.mark.django_db()
def test_delete_season_dont_exists(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")

    url = reverse("season-delete", kwargs={"season_id": 9999})
    response = client.delete(
        url
    )
    assert response.status_code == 404
    data = response.json().get("error")
    assert data == "Season does not exist"

@pytest.mark.django_db()
def test_create_episodie_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    
    payload = {
        "name": "Frutas en el centro & La bicicleta de Eugene", 
        "season": season.id,
        "original_name": "Downtown as fruits - Eugene 's bike",
        "original_date":"1996-08-17",
        "description":"Arnold y Gerald tienen que actuar vestidos como frutas en la obra escolar dirigida por Helga pero deciden no ir y terminan en el centro de la ciudad /// Arnold rompe accidentalmente la nueva bicicleta de Eugene así que trata de compensárselo pero todo lo que hace le sale mal.",
        "link1":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "link2":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "english":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "spoty":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "mediafire":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        }
    url = reverse("episodie-create")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    

@pytest.mark.django_db()
def test_create_episodie_wrong_name(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    
    payload = {
        "name": None, 
        "season":season.id,
        "original_name": "Downtown as fruits - Eugene 's bike",
        "original_date":"1996-08-17",
        "description":"Arnold y Gerald tienen que actuar vestidos como frutas en la obra escolar dirigida por Helga pero deciden no ir y terminan en el centro de la ciudad /// Arnold rompe accidentalmente la nueva bicicleta de Eugene así que trata de compensárselo pero todo lo que hace le sale mal.",
        "link1":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "link2":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "english":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "spoty":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "mediafire":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        }
    url = reverse("episodie-create")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 400
    
@pytest.mark.django_db()
def test_create_episodie_wrong_season(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    
    payload = {
        "name": "Frutas en el centro & La bicicleta de Eugene", 
        "season":99,
        "original_name": "Downtown as fruits - Eugene 's bike",
        "original_date":"1996-08-17",
        "description":"Arnold y Gerald tienen que actuar vestidos como frutas en la obra escolar dirigida por Helga pero deciden no ir y terminan en el centro de la ciudad /// Arnold rompe accidentalmente la nueva bicicleta de Eugene así que trata de compensárselo pero todo lo que hace le sale mal.",
        "link1":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "link2":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "english":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "spoty":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        "mediafire":"https://mega.nz/6046317f-22b4-483d-8671-ee88b4538106",
        }
    url = reverse("episodie-create")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 404
    error = response.json().get('error')
    assert error == 'Season does not exist'


@pytest.mark.django_db()
def test_update_episodie_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    season_2 = Season.objects.create(name="Temaporada 2")
    episodie = Episodies.objects.create(name="Frutas en el centro & La bicicleta de Eugene", season=season)
    
    payload = {
        "name": "Otro Nombre",
        "season":season_2.id,
        "original_name": None,
        "original_date":None,
        "description":None,
        "link1":None,
        "link2":None,
        "english":None,
        "spoty":None,
        "mediafire":None,
        }
    url = reverse("episodie-edit",kwargs={"episodie_id": episodie.id})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    result_episodie = Episodies.objects.get(id=episodie.id)
    assert result_episodie.name == "Otro Nombre"
    assert result_episodie.season == season_2


@pytest.mark.django_db()
def test_update_episodie_wrong_season(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    episodie = Episodies.objects.create(name="Frutas en el centro & La bicicleta de Eugene", season=season)
    
    payload = {
        "name": "Otro Nombre",
        "season":99,
        "original_name": None,
        "original_date":None,
        "description":None,
        "link1":None,
        "link2":None,
        "english":None,
        "spoty":None,
        "mediafire":None,
        }
    url = reverse("episodie-edit",kwargs={"episodie_id": episodie.id})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 404
    error = response.json().get('error')
    assert error == 'Season does not exist'
    
@pytest.mark.django_db()
def test_delete_episodie_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    episodie = Episodies.objects.create(name="Frutas en el centro & La bicicleta de Eugene", season=season)

    url = reverse("episodie-delete",kwargs={"episodie_id": episodie.id})
    response = client.delete(url)
    assert response.status_code == 200
    result_episodie = Episodies.objects.get(id=episodie.id)
    assert result_episodie.is_active == False
    message = response.json().get('message')
    assert message == 'Episodie deleted'

@pytest.mark.django_db()
def test_delete_episodie_wrog_id(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    season = Season.objects.create(name="Temaporada 1")
    episodie = Episodies.objects.create(name="Frutas en el centro & La bicicleta de Eugene", season=season)

    url = reverse("episodie-delete",kwargs={"episodie_id": 999})
    response = client.delete(url)
    assert response.status_code == 404
    error = response.json().get('error')
    assert error == 'Episodie does not exist'