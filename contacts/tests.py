from django.test import TestCase

from contacts.models import Contact

class ContactTests(TestCase):
    """Contact model tests."""

    def test_str(self):
        contact = Contact(first_name='Hayri', last_name='Cicek')

        self.assertEquals(str(contact), 'Hayri Cicek', )
