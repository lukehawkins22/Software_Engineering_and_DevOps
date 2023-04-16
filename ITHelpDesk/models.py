# References
# Django (no date) Models. Available at: https://docs.djangoproject.com/en/4.2/topics/db/models/ (Accessed: 16 April 2023).
# Stephen, N. (2022) What is __str__ in Django? . Available at: https://ngangasn.com/what-is-str-in-django-and-how-it-works/ (Accessed: 16 April 2023).

from django.db import models
from django.contrib.auth.models import User

#The below model is defining the Ticket model in the SQLite DB. This model represents a database table which is used to hold all ticket info.
#The first element of the class is to define set options which can be applied to the ticket_status field. These are open, blocked and closed.
#Below, the field definitions have been supplied, stating the field name and the data type and restrictions wich are applied to each field.
#Django(no date) 
class Ticket(models.Model):
    status_options = [
        ('Open', 'Open'),
        ('Blocked', 'Blocked'),
        ('Closed', 'Closed'),
    ]

    helpdesk_ticket_id = models.AutoField(primary_key=True) #PK
    ticket_title = models.CharField(max_length=200)
    ticket_description = models.TextField()
    ticket_user = models.ForeignKey(User, on_delete=models.CASCADE) #FK relationship to the user model. This will mean that if a user is deleted, the tickets created by that user will also be deleted
    ticket_status = models.CharField(max_length=50, choices=status_options, default='Open')
    ticket_time_created_at = models.DateTimeField(auto_now_add=True)
    ticket_time_updated_at = models.DateTimeField(auto_now=True)

    #This method states what should be returned of the ticket model is called upon within a method. It will return the ID of a ticket.
    #Stephen(2022)
    def __str__(self):
        return str(self.helpdesk_ticket_id)


#The below model is defining the Comment model in the SQLite DB. This model represents a database table which is used to hold all comment info.
#Below, the field definitions have been supplied, stating the field name and the data type and restrictions wich are applied to each field.
# Django(no date)
class Comment(models.Model):
    helpdesk_ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE) #FK relationship to the ticket model
    comment_text = models.TextField()
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE) #FK relationship to the user model
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_id = models.AutoField(primary_key=True) #PK

    #This method states what should be returned of the comment model is called upon within a method. It will return the text of a ticket.
    #Stephen(2022)
    def __str__(self):
        return self.comment_text

