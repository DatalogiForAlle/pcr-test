# Create your tests here.
from django.test import TestCase, SimpleTestCase
from ..forms import DNAForm, ForwardPrimerForm



class ForwardPrimerFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "start": 12,
            "length": 10
        } 

    def test_market_created(self):
        """ Valid data gives valid form."""
        len_dna = 44
        form = ForwardPrimerForm(len_dna, data=self.valid_data)
        assert form.is_valid()


    def test_clean_dna_primer_min_length(self):
        """ primer length cannot be shorter than 5 letters """
        self.valid_data["length"] = 4
        len_dna = 44
        form = ForwardPrimerForm(len_dna, data=self.valid_data)

        assert not form.is_valid()
        assert 'length' in form.errors
        assert 'Denne værdi skal være større end eller lig 5.' in str(
            form.errors)

    def test_sum_of_length_plus_start_to_big(self):
        """"
        Primer start + length not to big for dna
        DNA:      AAAAAA
        Primer:  PPPPP
        """

        dna = "AAAAAA"
        self.valid_data["start"] = 3 # primer will start at third letter from right
        self.valid_data["length"] = 5  
        form = ForwardPrimerForm(len(dna), data=self.valid_data)

        assert not form.is_valid()
        assert 'DNA-strengen er for kort til dine valg for primeren' in str(
            form.errors)

    def test_sum_of_length_plus_start_not_to_big(self):
        """ 
        Primer start + length not to big for dna 
        DNA:      AAAAAAA
        Primer:   PPPPP
        """
        dna  = "AAAAAAA"
        self.valid_data["start"] = 3
        self.valid_data["length"] = 5
        form = ForwardPrimerForm(len(dna), data=self.valid_data)

        assert form.is_valid()
        