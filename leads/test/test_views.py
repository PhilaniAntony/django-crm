from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.


class HomePageTest(TestCase):
    def test_get(self):
        response = self.client.get(reversed('landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home-page.html')
