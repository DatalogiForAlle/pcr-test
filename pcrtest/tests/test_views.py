from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class HomeViewGetRequestTests(SimpleTestCase):
    def test_home_page_status_code(self):
        """ Home page exists at proper url and uses correct template """
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pcrtest/home.html')

class HomeViewPostRequestTests(TestCase):
    pass