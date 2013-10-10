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
        self.client.login(username=self.user.username, password='rosedu')

    def test_profile_is_created_with_non_existing_username(self):
        """Assert that if the profile-create view is populated with a unique
        username the profile is created."""

        self.person_data['username'] = 'john'
        resp = self.client.post(reverse('profile-create'), self.person_data)
        person_count = Person.objects.count()
        self.assertEqual(2, person_count)

    def test_profile_is_not_created_with_password2_missing(self):
        """Assert that if the profile-create view is populated with password2
        missing, the profile is not created."""

        self.person_data['username'] = 'john'
        self.person_data.pop('password2')
        response = self.client.post(reverse('profile-create'), self.person_data)
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')

    def test_profile_is_not_created_with_passwords_not_matching(self):
        """Assert that if the profile-create view is populated with passwords
        not matching, the profile is not created."""

        self.person_data['username'] = 'john'
        self.person_data['password2'] = 'rosedu1'
        response = self.client.post(reverse('profile-create'), self.person_data)
        self.assertFormError(response, 'form', 'password2',
                             'The two password fields didn\'t match.')

    def test_profile_is_not_created_with_existing_username(self):
        """Assert that if the profile-create view is populated with a
        non-unique username the profile is not created."""

        self.person_data['username'] = self.user.username
        response = self.client.post(reverse('profile-create'), self.person_data)
        self.assertFormError(response, 'form', 'username',
                             'A user with that username already exists.')
