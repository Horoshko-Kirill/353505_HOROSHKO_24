import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from shop.models import Client, Employee, Manufacturer, Order, OrderItem, JobVacancy, FAQItem, AboutCompany


pytestmark = pytest.mark.django_db

def test_home_page(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'calendar' in response.context
    assert 'jokes' in response.context


def test_about_page(client):
    response = client.get(reverse('about'))
    assert response.status_code == 200


@pytest.fixture
def employee():
    user = User.objects.create_user(username='emp', password='pass')
    return Employee.objects.create(user=user, department='IT', position='Dev', is_visible=True)

@pytest.fixture
def vacancy():
    return JobVacancy.objects.create(title="Python Dev", is_active=True)

def test_careers_page(client, vacancy):
    response = client.get(reverse('careers'))
    assert response.status_code == 200
    assert vacancy in response.context['vacancies']


@pytest.fixture
def vacancy():
    return JobVacancy.objects.create(title="Python Dev", is_active=True)

def test_careers_page(client, vacancy):
    response = client.get(reverse('careers'))
    assert response.status_code == 200
    assert vacancy in response.context['vacancies']


@pytest.fixture
def client_user():
    user = User.objects.create_user(username='clientuser', password='pass')
    group = Group.objects.get_or_create(name='client')[0]
    user.groups.add(group)
    client_obj = Client.objects.create(user=user)
    return user, client_obj


def test_login_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

def test_login_post_success(client, django_user_model):
    user = django_user_model.objects.create_user(username='test', password='pass')
    response = client.post(reverse('login'), {'username': 'test', 'password': 'pass'})
    assert response.status_code == 302  # redirect to home

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='admin', password='admin')

def test_manufacturers_page(client):
    response = client.get(reverse('manufacturers'))
    assert response.status_code == 200

def test_add_manufacturer_requires_admin(client):
    response = client.get(reverse('add_manufacturer'))
    assert response.status_code in (302, 403)

def test_add_manufacturer_as_admin(client, admin_user):
    client.login(username='admin', password='admin')
    response = client.get(reverse('add_manufacturer'))
    assert response.status_code == 200
