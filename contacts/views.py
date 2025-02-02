from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from contacts.models import Contact
# Create your views here.
class ContactListView(generic.ListView):
    model = Contact
    
class ContactCreateView(generic.CreateView):
    model = Contact
    fields = ('avatar', 'name', 'email', 'birth', 'phone',)
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(generic.UpdateView):
    model = Contact
    fields = ('avatar', 'name', 'email', 'birth', 'phone',)
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')