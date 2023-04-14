from django.contrib import admin
from .models import Ticket, Comment 

#The below class TicketAdminDisplay handles the creation of the Django Admin view for the Ticket model.
#It will show the specified fields below in the Admin interface.
#The search fields will provide admins wwith a search field interface 
class TicketAdminDisplay(admin.ModelAdmin):
    list_display = ('helpdesk_ticket_id', 'ticket_title', 'ticket_description', 'ticket_user', 'ticket_status', 'ticket_time_created_at', 'ticket_time_updated_at')
    search_fields = ['helpdesk_ticket_id'] 

#The below class CommentAdminDisplay handles the creation of the Django Admin view for the Ticket model.
#It will show the specified fields below in the Admin interface.
#The search fields will provide admins wwith a search field interface 
class CommentAdminDisplay(admin.ModelAdmin):
    list_display = ('helpdesk_ticket_id', 'comment_text', 'comment_user', 'comment_created_at')
    search_fields = ['helpdesk_ticket_id__helpdesk_ticket_id']  # search by the Ticket ID

#The below then registers the models on the Django admin interface with the relevent class defining fields to show.
admin.site.register(Ticket, TicketAdminDisplay)
admin.site.register(Comment, CommentAdminDisplay)