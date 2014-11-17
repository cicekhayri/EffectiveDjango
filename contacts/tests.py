from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from rebar.testing import flatten_to_dict

from contacts import forms
from contacts.models import Contact

class ContactTests(TestCase):
    """Contact model tests."""

    def test_str(self):
        contact = Contact(first_name='Hayri', last_name='Cicek')

        self.assertEquals(str(contact), 'Hayri Cicek', )

class ContactListIntegrationTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTest, cls).tearDownClass()

    def test_contact_listed(self):
        # create a test contact
        Contact.objects.create(first_name='foo', last_name='bar')

        # make sure it's listed as <first> <last> on the list
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(self.selenium.find_elements_by_css_selector('.contact')[0].text, 'foo bar')

    def test_add_contact_linked(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(self.selenium.find_element_by_link_text('add contact'))

    def test_add_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()
        
        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')

        self.selenium.find_element_by_id("save_contact").click()
        self.assertEqual(self.selenium.find_elements_by_css_selector('.contact')[-1].text, 'test contact')

class EditContactFormTest(TestCase):
    def test_mismatch_email_is_invalid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'bar@example.com'

        bound_form = forms.ContactForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

    def test_same_email_is_valid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'foo@example.com'

        bound_form = forms.ContactForm(data=form_data)
        self.assert_(bound_form.is_valid())

