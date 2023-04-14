import pytest
from django.urls import reverse
from django.test import Client
from django.http import response
from django.contrib.auth.models import User
from ITHelpDesk.models import Ticket, Comment

#pytest ITHelpDesk\tests\test_views.py -v -c ITHelpDesk\tests\pytest.ini

#Test to confirm that the home view displays the correct content if the user is not authenticated.
def test_home_not_authenticated(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert b'To Make Use of This System, You Need to be Logged In' in response.content
    assert 'ITHelpDesk/home.html' in [t.name for t in response.templates]

#Test to confirm that the home view displays the correct content if the user is authenticated.
@pytest.mark.django_db
def test_home_authenticated(client):

    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    client.login(username='pytestuser', password='Password1')

    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert b'User Dashboard' in response.content
    assert 'ITHelpDesk/home.html' in [t.name for t in response.templates]

#Test to confirm that the correct data is presented when the login view is called upon. 
def test_login(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Please supply the following information, then press &quot;Login&quot' in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]

#Test to confirm that the correct data is presented when the login view is called upon.
def test_signup(client):
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200
    assert b"To create a new user account, please supply the following information" in response.content
    assert 'registration/signup.html' in [t.name for t in response.templates]

#Test to confirm that the correct data is presented when the create ticket view is called upon as an authenticated user.
@pytest.mark.django_db
def test_create_ticket_authenticated(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    client.login(username='pytestuser', password='Password1')

    url = reverse('create-ticket')
    response = client.get(url)
    assert response.status_code == 200
    assert b"To create a new helpdesk ticket, please enter the following information" in response.content
    assert 'ITHelpDesk/helpdesk_create_ticket.html' in [t.name for t in response.templates]

#Test to confirm that the correct HTTP 302 redirect is presented when an unauthenticated user attempts to access the create ticket view.
@pytest.mark.django_db
def test_create_ticket_unauthenticated(client):
    url = reverse('create-ticket')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert b"Please supply the following information, then press &quot;Login&quot" in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the edit ticket view is called with a valid url PK. 
@pytest.mark.django_db
def test_edit_ticket_authenticated_correct_PK(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    ticket = Ticket.objects.create(
        ticket_title='Test Ticket',
        ticket_description='this is a test ticket',
        ticket_user=user,
        ticket_status='Open',
    )

    client.login(username='pytestuser', password='Password1')

    response = client.get(f'/edit-ticket/{ticket.pk}', follow=True)
    assert response.status_code == 200
    assert b"To edit the helpdesk ticket, please make the changes below." in response.content
    assert 'ITHelpDesk/helpdesk_edit_ticket.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the edit ticket view is called with an invalid url PK. 
@pytest.mark.django_db
def test_edit_ticket_authenticated_incorrect_PK(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    client.login(username='pytestuser', password='Password1')

    response = client.get(f'/edit-ticket/', follow=True)
    assert response.status_code == 200
    assert b"Below, please see all IT Helpdesk Tickets that have been raised." in response.content
    assert 'ITHelpDesk/helpdesk_view_all_tickets.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the edit ticket view is called unauthenticated. 
@pytest.mark.django_db
def test_edit_ticket_unauthenticated(client):
    response = client.get(f'/edit-ticket/', follow=True)
    assert response.status_code == 200
    assert b"Please supply the following information, then press &quot;Login&quot" in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the view all tickets view is called unauthenticated. 
@pytest.mark.django_db
def test_view_all_tickets_unauthenticated(client):
    url = reverse('view-all-tickets')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert b"Please supply the following information, then press &quot;Login&quot" in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]

#Test to confirm that the correct data is presented when the view all tickets view is called upon as an authenticated user.
@pytest.mark.django_db
def test_view_all_tickets_authenticated(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    client.login(username='pytestuser', password='Password1')

    url = reverse('view-all-tickets')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert b"Below, please see all IT Helpdesk Tickets that have been raised." in response.content
    assert 'ITHelpDesk/helpdesk_view_all_tickets.html' in [t.name for t in response.templates]

#Test to confirm that the correct data is presented when the view my tickets view is called upon as an authenticated user.
@pytest.mark.django_db
def test_view_my_tickets_authenticated(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )
    
    ticket = Ticket.objects.create(
        ticket_title='Test Ticket for unit test',
        ticket_description='this is a test ticket',
        ticket_user=user,
        ticket_status='Open',
    )

    client.login(username='pytestuser', password='Password1')

    url = reverse('view-my-tickets')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert b"Test Ticket for unit test" in response.content
    assert 'ITHelpDesk/helpdesk_view_user_tickets.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the view my tickets view is called unauthenticated. 
@pytest.mark.django_db
def test_view_my_tickets_unauthenticated(client):
    url = reverse('view-my-tickets')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert b"Please supply the following information, then press &quot;Login&quot" in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the add comment view is called with a valid url PK. 
@pytest.mark.django_db
def test_add_comment_authenticated_correct_PK(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    ticket = Ticket.objects.create(
        ticket_title='Test Ticket',
        ticket_description='this is a test ticket',
        ticket_user=user,
        ticket_status='Open',
    )

    client.login(username='pytestuser', password='Password1')

    response = client.get(f'/edit-ticket/{ticket.pk}/add-comment', follow=True)
    assert response.status_code == 200
    assert b"Please add your comment below." in response.content
    assert 'ITHelpDesk/helpdesk_add_comment.html' in [t.name for t in response.templates]

#Test to confirm that the correct view is displayed when the add comment view is called with a invalid url PK. 
@pytest.mark.django_db
def test_add_comment_authenticated_incorrect_PK(client):
    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )

    client.login(username='pytestuser', password='Password1')
    with pytest.raises(Ticket.DoesNotExist):
        response = client.get(f'/edit-ticket/50000000/add-comment', follow=True)

#Test to confirm that the correct view is displayed when the add comment view is called unauthenticated. 
@pytest.mark.django_db
def test_add_comment_unauthenticated(client):
    response = client.get(f'/edit-ticket/5000000/add-comment', follow=True)
    assert response.status_code == 200
    assert b"Please supply the following information, then press &quot;Login&quot" in response.content
    assert 'registration/login.html' in [t.name for t in response.templates]