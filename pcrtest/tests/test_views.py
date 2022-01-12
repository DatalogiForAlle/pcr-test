from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class ForwardViewTests(SimpleTestCase):
    def test_forward_page_status_code(self):
        """ Forward primer page exists at proper url and uses correct template """
        response = self.client.get(reverse('forward-primer'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pcrtest/forward.html')

class HomePageViewTests(SimpleTestCase):
    def test_home_page_redirects(self):
        """ Home page should redirect to forward-primer page """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertEquals(response['Location'], reverse(
                'forward-primer'))


class ReverseViewTests(SimpleTestCase):
    def test_reverse_page_status_code(self):
        """ Reverse primer page exists at proper url and uses correct template """
        data = {'upper_dna': '', 'forward_primer_start': 0, 'forward_primer_length': 0}

        response = self.client.post(reverse('reverse-primer'), data = data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pcrtest/reverse.html')
