# References
# Django (no date) URL dispatcher. Available at: https://docs.djangoproject.com/en/4.2/topics/http/urls/ (Accessed: 16 April 2023).

from django.urls import path
from ITHelpDesk import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#The below URL patterns are used to directs users and requests to the URL based on what I supply, and also define what view should be 
#supplied for each view. 
#For example, when I supply the hosturl:8000/home, the home view will be rendered. Where views are defined as classes, I am showing the class as_view.
#Django(no date) 
urlpatterns = [
    path("home/", views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("create-ticket/", views.CreateHelpdeskTicket.as_view(), name="create-ticket"),
    path("edit-ticket/<int:pk>/", views.EditHelpdeskTicket.as_view(), name="edit-ticket"),
    path('edit-ticket/<int:pk>/add-comment/', views.AddTicketComment.as_view(), name='add-comment'),
    path("view-my-tickets/", views.view_user_tickets, name="view-my-tickets"),
    path("view-all-tickets/", views.view_all_tickets, name="view-all-tickets"),
    path("edit-ticket/", views.view_all_tickets, name="edit-ticket"),
    path("", views.home, name="home"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)