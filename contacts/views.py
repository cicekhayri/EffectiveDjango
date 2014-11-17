from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView

from contacts.models import Contact

class ListContactView(ListView):
    model = Contact
    template_name = 'contact_list.html'

class CreateContactView(CreateView):
    model = Contact
    template_name = 'edit_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')
