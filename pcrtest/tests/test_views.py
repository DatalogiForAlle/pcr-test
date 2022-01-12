from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class ForwardViewGetRequestTests(SimpleTestCase):
    def test_forward_page_status_code(self):
        """ Forward primer page exists at proper url and uses correct template """
        response = self.client.get(reverse('forward-primer'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pcrtest/forward.html')

class ForwardViewPostRequestTests(TestCase):
    pass

class ReverseViewPOSTRequestTests(SimpleTestCase):
    def test_reverse_page_status_code(self):
        """ Reverse primer page exists at proper url and uses correct template """
        response = self.client.post(reverse('reverse-primer'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pcrtest/reverse.html')
