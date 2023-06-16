import pytest
from rest_framework.test import APIClient

client = APIClient()
@pytest.mark.django_db
def test_registerApi():
    
    payload = {
    "first_name": "gio",
    "last_name": "sani",
    "email": "g@g.com",
    "password": "123",
    "password_confirm": "123",
    "is_company_owner": "True",
    "is_company_member": "False"
    }

    response = client.post('/api/register',payload)

    data = response.data
    print('tests===',data)
    assert data['first_name'] == payload['first_name']

    login_payload = {
        "email": "g@g.com",
        "password": "123",
        "scope": "company_owner"

    }

    response = client.post('/api/login',login_payload)
    data = response.data

    assert response.status_code == 200
    # response = client.delete(f'/api/user/delete/{response.data["id"]}')

    # assert response.status_code == 204, f'expected 204 but got {response.status_code} - {response.data}'


# @pytest.mark.django_db
# def test_delete_user():
#     # Create a test user
#     user = user_factory()

#     response = client.delete(f'/api/user/delete/{user.pk}')

#     assert response.status_code == 204, f'expected 204 but got {response.status_code} - {response.data}'

