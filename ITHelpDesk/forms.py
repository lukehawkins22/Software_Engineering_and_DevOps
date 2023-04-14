from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Comment

#The below class defines the Django form which I have used to create a user within the Django User model.
#There is already a predefined UserCreationForm as part of the Django framework.
#I have expanded the functionlaity of this form, creating HelpdeskUserCreationForm, which also collects email, firstname and lastname details.
class HelpdeskUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter your email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    
    #The meta class is used to confingure uniquely the respective form fields stored within the model.
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )


#The below class creates a form to be displayed in the UI which handles the creation and edits of Tickets stored within the ticket model.
#The form only needs to collect 2 of the fields from the user, these being the title and the description. The others are autofilled by the model.
#The ticket_title and ticket_description fields have certain restrctions around them which must be met for the form to be submitted.
class TicketForm(forms.ModelForm):
    ticket_title = forms.CharField(max_length=1000, required=True, help_text='Required.')
    ticket_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), max_length=1000, required=True, help_text='Required.')
    
    #The meta class is used to confingure uniquely the respective form fields stored within the model.
    class Meta:
        model = Ticket
        fields = ['ticket_title', 'ticket_description']

    #The save method is used to tell the application what to do once the form is submitted. Once submitted, it saves the instance, ie the updated model.
    #It also checks whether a user can edit an existing object in the model, by comparing the logged in UserID to that of the one registered on the ticket.
    def save(self, commit=True, request=None):
        instance = super().save(commit=False)
        if request:
            instance.ticket_user = request.user
        if commit:
            instance.save()
        #Once the if statement has been satified, the saved instance is returned to the interface for viewing.
        return instance

#The below class creates a form to be displayed in the UI which handles the creation of comments stored within the comment model.
#The form only needs to collect 1 of the field from the user, these being the comment text. The others are autofilled by the model.
#The comment_text field has certain restrctions around it which must be met for the form to be submitted.

class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), max_length=500, required=True)

    #The meta class is used to confingure uniquely the respective form fields stored within the model.
    class Meta:
        model = Comment
        fields = ('comment_text',)



