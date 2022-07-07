import json

from flask import url_for

from pinterest.models import User

from base64 import b64encode


def test_register_route(client, captured_templates) -> None:
    route = "/register"
    rv = client.get(route)
    pv = client.post(route)

    assert rv.status_code == 200
    assert pv.status_code == 200
    assert len(captured_templates) == 2
    template, context = captured_templates[0]
    assert template.name == "register.html"

    assert context['title'] == 'register'


def test_add_user(client):
    """Ensure a new user can be added to the database."""

    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='viral',
            email='viral@realpython.com',
            password=None
        )),
        content_type='application/json',
    )
    data = response.data
    print(data)
    # assert response.status_code == 201
    # assert 'viral@realpython.com was added!' in data['message']
    # assert 'success' in data['status']


def test_login_route(client, captured_templates) -> None:
    route = "/login"
    user = User.query.all()
    print(f"USER {user}")

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'payload': {
            "email": "chitrangda15@gmail.com",
            "password": "idk"
        }
    }

    response = client.post(route, data=json.dumps(mock_request_data), headers=mock_request_headers)
    print(f'-----------------response {response}')
    assert response.status_code == 200


def test_main_page(client, captured_templates):
    url = "/pin/views"
    response = client.get(url)
    print(response.get_data())


def test_protected_route(client):
    credentials = b64encode(b"user:password").decode("utf-8")
    route = "/register"
    rv = client.get(route, headers={"Authorization": "Basic " + credentials})
    assert rv.status_code == 200


#     rv = client.get(route, data=data)
#     pv = client.post(route, data=data, headers=headers)
#     print(f"PV {pv}")
#
#     # assert rv.status_code == 200
#     assert pv.status_code == 200
# assert len(captured_templates) == 2
# template, context = captured_templates[0]
# assert template.name == "login.html"
#
# assert context['title'] == 'loginn'
from pinterest.users.routes import users


def test_post_request(client):
    def get_endpoint():
        return url_for('users.login', _external=True)

    res = client.post(
        get_endpoint(),
        # headers={'Content-Type': 'application/json'},
        data={"email": "chitrangda15@gmail.com",
              "password": "hbh123Hbbb"}
    )

    assert res.status_code == 200


def test_logout(client, captured_templates) -> None:
    route = 'users.logout'

    rv = client.get(route)

    pv = client.post(route)
    assert client.get(url_for(route)).status_code == 302
    # assert rv.status_code == 302
    # assert pv.status_code == 405

# def test_data_insert(client, captured_templates):
#     route = 'http://127.0.0.1:5000/account'
#     data = {
#         "username": "viral"
#     }
#     pv = client.post(route, data=data)
#     print(pv)


# def test_pin_board(client, captured_templates):
#     # route = "/board/create"
#     data = {'email':'chitrangda@gmail.com', 'password':'hb123H@bbb'}
#     response = client.post('/login', data=data,
#                            headers={'Content-Type': 'json'}
#                            )
#     print(response)
