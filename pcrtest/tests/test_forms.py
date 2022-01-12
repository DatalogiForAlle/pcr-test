# Create your tests here.
from django.test import TestCase, SimpleTestCase
from ..forms import ForwardPrimerForm


class ForwardPrimerFormTests(TestCase):


    def setUp(self):
        self.valid_data = {
            "dna": "TGGCCTtgaGTGGGTCCCCCCATAGATCATAAGCCCA",
            "start": 12,
            "length": 10
        } 

    def test_market_created(self):
        """ Valid data gives valid form."""
        form = ForwardPrimerForm(data=self.valid_data)
        assert form.is_valid()

    def test_clean_dna_letters_1(self):
        """ DNA string should only consist of A, C, T and G's """
        self.valid_data["dna"] = "XTCCAAA"
        form = ForwardPrimerForm(data=self.valid_data)
   
        assert not form.is_valid()
        assert 'dna' in form.errors
        assert 'DNA-strengen må kun indeholde bogstaverne A, C, G og T.' in str(form.errors)

    def test_clean_dna_letters_2(self):
        """ DNA string should only consist of A, C, T and G's """
        self.valid_data["dna"] = "TCCxAAA"
        form = ForwardPrimerForm(data=self.valid_data)

        assert not form.is_valid()
        assert 'dna' in form.errors
        assert 'DNA-strengen må kun indeholde bogstaverne A, C, G og T.' in str(
            form.errors)

    def test_clean_dna_min_length(self):
        """ DNA cannot be shorter than 5 letters """
        self.valid_data["dna"] = "AAAC"
        form = ForwardPrimerForm(data=self.valid_data)

        assert not form.is_valid()
        assert 'dna' in form.errors
        assert 'DNA-streng er for kort.' in str(
            form.errors)

    def test_clean_dna_primer_min_length(self):
        """ primer length cannot be shorter than 5 letters """
        self.valid_data["length"] = 4
        form = ForwardPrimerForm(data=self.valid_data)

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

        self.valid_data["dna"] = "AAAAAA"
        self.valid_data["start"] = 3 # primer will start at third letter from right
        self.valid_data["length"] = 5  
        form = ForwardPrimerForm(data=self.valid_data)

        assert not form.is_valid()
        assert 'DNA-strengen er for kort til dine valg for primeren' in str(
            form.errors)

    def test_sum_of_length_plus_start_not_to_big(self):
        """ 
        Primer start + length not to big for dna 
        DNA:      AAAAAAA
        Primer:   PPPPP
        """
        self.valid_data["dna"] = "AAAAAAA"
        self.valid_data["start"] = 3
        self.valid_data["length"] = 5
        form = ForwardPrimerForm(data=self.valid_data)

        assert form.is_valid()
        