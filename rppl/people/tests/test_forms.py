from django.test import TestCase, Client
from django.core.urlresolvers import reverse


from people.factories.person_factory import PersonFactory
from people.models import Person


class TestProfileCreateForm(TestCase):


    def setUp(self):
        self.person_data = {
            'username': 'Bobby',
            'password1': 'rosedu',
            'password2': 'rosedu',
            'first_name': 'Robert',
            'last_name': 'Fischer',
            'email': 'Bobby@Fischer.com'
        }
        self.client = Client()
        self.user = PersonFactory()
        self.client.login(username='john', password='rosedu')

    def test_profile_create_good(self):
        resp = self.client.post(reverse('profile-create'), self.person_data)
        person_count = Person.objects.count()
        self.assertEqual(2, person_count)


    def test_profile_create_bad(self):
        self.person_data.pop('password2')
        response = self.client.post(reverse('profile-create'), self.person_data)
        error_count = response.content.count('errorlist')
        self.assertEqual(2, error_count)

    def test_bad_username_bad(self):
        self.person_data['username'] = 'john'
        response = self.client.post(reverse('profile-create'), self.person_data)
        error_count = response.content.count('<li>username')
        self.assertEqual(1, error_count)