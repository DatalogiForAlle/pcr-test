# Create your tests here.
from django.test import TestCase
from ..forms import SqlForm
from django.core.exceptions import ValidationError


class SqlFormtests(TestCase):

    def test_insert_forbidden_upper_case(self):
        """ INSERT statements are invalid """
        sql = "blah blah INSERT blah blah"
        form = SqlForm(data={'sql': sql})

        is_valid = form.is_valid()

        self.assertFalse(is_valid)
        assert 'Du har ikke tilladelse til at udføre INSERT-operationer' in str(
            form.errors)

  