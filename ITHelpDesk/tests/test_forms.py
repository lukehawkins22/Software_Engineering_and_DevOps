import pytest
from django.urls import reverse
from django.test import Client
from django.http import response
from django.contrib.auth.models import User
from ITHelpDesk.models import Ticket, Comment
#pytest ITHelpDesk\tests\test_forms.py -v -c ITHelpDesk\tests\pytest.ini


#This test is used to show ensure that the form used on the create ticket page is able to create a new db object as expected. 
@pytest.mark.django_db
def test_create_ticket(client):

    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )
    client.login(username='pytestuser', password='Password1')

    response = client.post(reverse('create-ticket'), data={
        'ticket_title': 'Unit Test',
        'ticket_description': 'this is a unit test ticket',
    })
    assert response.status_code == 302
    assert Ticket.objects.count() == 1
    unit_ticket = Ticket.objects.first()
    assert unit_ticket.ticket_title == 'Unit Test'
    assert unit_ticket.ticket_description == 'this is a unit test ticket'

#This test is used to show ensure that the form used on the create comment page is able to create a new db comment object as expected. 
@pytest.mark.django_db
def test_create_comment(client):

    user = User.objects.create_user(
        username='pytestuser',
        password='Password1',
    )
    client.login(username='pytestuser', password='Password1')

    ticket = Ticket.objects.create(
        ticket_title='Test Ticket',
        ticket_description='this is a test ticket',
        ticket_user=user,
        ticket_status='Open',
    )
    
    response = client.post(f'/edit-ticket/{ticket.pk}/add-comment/', data={
        'comment_text': 'this is a unit test comment',
    })
    print(ticket.pk)

    assert response.status_code == 302
    assert Comment.objects.count() == 1
    unit_comment = Comment.objects.first()
    assert unit_comment.comment_text == 'this is a unit test comment'

