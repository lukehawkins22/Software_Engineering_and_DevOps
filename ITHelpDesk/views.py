from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.http import Http404
from django.urls import reverse_lazy
from .forms import HelpdeskUserCreationForm
from .forms import TicketForm
from .forms import CommentForm
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from .models import Ticket
from .models import Comment
from django.contrib import messages

# Create your views here.

#The below view definition handles the rendering and display of the home view.
#When the home view is called, it will display home.html file.
def home(request):
    if request.user.is_authenticated:
        open_tickets = Ticket.objects.filter(ticket_user=request.user, ticket_status='Open').count()
        total_tickets = Ticket.objects.filter(ticket_user=request.user).count()
    else:
        open_tickets = 0
        total_tickets = 0
    return render(request, 'ITHelpDesk/home.html', {'total_tickets': total_tickets, 'open_tickets': open_tickets})

#The below class is used to handle all logic required for the user sign up page to be funtional. It provides the HelpdeskUserCreationForm
#to be rendered, and also defines what should happen if the form submission is a success. In this case, it will redirect to the login view.
#It also states which HTML should be rendered when the class is called as a view. It renders signup.html
class SignUp(CreateView):
    form_class = HelpdeskUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

#The below class is used to handle all logic required for the ticket creation page to be functional. It provides the TicketForm
#to be rendered, and also defines what should happen if the form submission is a success. In this case, it will redirect to the home view.
#It also states which HTML should be rendered when the class is called as a view. It renders helpdesk_create_ticket.html
#It also uses the LoginRequiredMixin which ensures a user is logged in to view the form. 
class CreateHelpdeskTicket(LoginRequiredMixin, CreateView):
    form_class = TicketForm
    success_url = reverse_lazy("view-my-tickets")
    template_name = "ITHelpDesk/helpdesk_create_ticket.html"
    
    #The below method checks whether the form meets the required criteria defined within the forms.py, then runs the save method.
    #It also will display a success message on the page which the user is redirected to when the form is submitted.
    def form_valid(self, form):
        messages.success(self.request, 'Your ticket was successfully created.')
        form.save(request=self.request)
        return super().form_valid(form)
    
#The below class is used to handle all logic required for the ticket edit page to be functional. It provides the TicketForm
#to be rendered, and also defines what should happen if the form submission is a success. In this case, it will redirect to the home view.
#It also states which HTML should be rendered when the class is called as a view. It renders helpdesk_edit_ticket.html. 
#This view is also needed to supply the relevent information from the Ticket model based on the ID which is passed into the URL.
class EditHelpdeskTicket(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = TicketForm
    model = Ticket
    success_url = reverse_lazy("view-my-tickets")
    template_name = "ITHelpDesk/helpdesk_edit_ticket.html"

    # def get_object(self, queryset=None):
    #     try:
    #         return super().get_object(queryset)
    #     except Http404:
    #         return None

    #This test is used to check if the logged in user matches that of the user ID resgistered for the ticket model being edited.
    #It returns a true of false bool. If it is false, the request is not valid and forbidden. The handling of a false reponse is 
    #dealt with within the below method.
    def test_func(self):
        ticket_check = self.get_object()
        if self.request.user == ticket_check.ticket_user:
            return True
        else:
            return False

    #This test is used to check if there is a logged in user. If there is no logged in user, they are redirected the login view. 
    #If the user is logged in, they are displayed the not_authorised.html    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden(render(self.request, 'ITHelpDesk/not_authorised.html'))
        else:
            return redirect('login')

    #The below method checks whether the form meets the required criteria defined within the forms.py, then runs the save method.
    #It also will display a success message on the page which the user is redirected to when the form is submitted.
    def form_valid(self, form):
        messages.success(self.request, 'Your ticket was successfully updated.')
        form.save(commit=True, request=self.request)
        return super().form_valid(form)
    
#The below view definition handles the rendering and display of the view_user_tickets view.
#When the view is called, it will display helpdesk_view_user_tickets.html file. It also filters the display so that it shows 
#only tickets matching the logged in users ID.
@login_required #The user must be logged in for the view to be rendered.
def view_user_tickets(request):
    userTickets = Ticket.objects.filter(ticket_user=request.user)
    return render(request, 'ITHelpDesk/helpdesk_view_user_tickets.html', {'userTickets': userTickets})

#The below view definition handles the rendering and display of the view_all_tickets view.
#When the view is called, it will display helpdesk_view_all_tickets.html file. 
@login_required #The user must be logged in for the view to be rendered.
def view_all_tickets(request):
    allTickets = Ticket.objects.all()
    return render(request, 'ITHelpDesk/helpdesk_view_all_tickets.html', {'allTickets': allTickets})

#The below class is used to handle all logic required for the add comment page to be functional. It provides the CommentForm
#to be rendered, and also defines what should happen if the form submission is a success. 
#In this case, it will redirect to the edit ticket page relating to the relevant ticket.
#It also states which HTML should be rendered when the class is called as a view. It renders helpdesk_add_comment.html. 
#This view is also needed to supply the relevent information from the comment model based on the ticket ID which is passed into the URL.
class AddTicketComment(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'ITHelpDesk/helpdesk_add_comment.html'

    #This test is used to check if the ticketID of the ticket which the comment is linked to matches that of the logged in users ID.
    #It also checks that the ticket itsef exists.
    def test_func(self):
        ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        return self.request.user == ticket.ticket_user

    #The below method sets the comment_user equal to that of the logged in user. It also sets the ticket ID to that of the PK from the URL.
    #It will display a success message on the success page when the form is successfully submitted and redirect to the edit ticket page for that ticket. 
    def form_valid(self, form):
        form.instance.comment_user = self.request.user
        form.instance.helpdesk_ticket_id_id = self.kwargs['pk']
        messages.success(self.request, 'Your comment was successfully added.')
        self.success_url = reverse_lazy('edit-ticket', args=[self.kwargs['pk']])
        return super().form_valid(form)
    
    #This test is used to check if there is a logged in user. If there is no logged in user, they are redirected the login view. 
    #If the user is logged in, they are displayed the not_authorised.html   
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden(render(self.request, 'ITHelpDesk/not_authorised.html'))
        else:
            return redirect('login')

def handler404(request, exception):
    return render(request, 'ITHelpDesk/page_not_found.html', status=404)

def handler400(request, exception):
    return render(request, 'ITHelpDesk/page_not_found.html', status=400)

def handler500(request):
    return render(request, 'ITHelpDesk/page_not_found.html', status=500)