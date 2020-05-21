from django.test import TestCase
from .models import Projekti

# Create your tests here.


class ProjektiTestCase(TestCase):
    def setUp(self):
        Projekti.objects.create(title="lion", shortdescription="roar")
        Projekti.objects.create(title="cat", shortdescription="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Projekti.objects.get(title="lion")
        cat = Projekti.objects.get(title="cat")
        self.assertEqual(lion.description(), 'The lion says "roar"')
        self.assertEqual(cat.description(), 'The cat says "meow"')