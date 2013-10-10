import factory

from django.contrib.auth.hashers import make_password

from people.models import Person


class PersonFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = Person

    first_name = 'John'
    last_name = 'Doe'
    username = factory.Sequence(lambda n: 'John%s' % n)
    email = 'john@rosedu.org'
    password = make_password('rosedu')

    is_superuser = True
