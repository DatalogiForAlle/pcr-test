from django import forms

class PrimerForm(forms.Form):
    
    dna = forms.CharField(max_length=300, label="Øvre DNA-streng", initial="TGGCCTGTGGGTCCCCCCATAGATCATAAGCCCAGGAGGAAGGGCTGTGTTTCAGGGCTGTGATCACTAGCACCCAGAACCGTCGACTGGCACAGAACAGGCACTTAGGGAACCCTCACTGAATGAATGAATGAATGAATGAATGAATGAATGTTTGGGCAAATAAACGCTGACAAGGACAGAAGGGCCTAGCGGGAAGGG",
                                    help_text="Indtast den øvre del af DNA-streng")

    start = forms.IntegerField(label="Primer start",
                                initial=21,
                               help_text="Ved hvilken baseposition (talt fra venstre) skal din primer begynde? Angiv et heltal på mindst 1.",
                               min_value=1
                               )
    length = forms.IntegerField(label="Primer længde", min_value=5, initial=21,
                               help_text="Hvor mange baser skal din primer bestå af? Angiv et heltal på mindst 5.")


    # start-værdi + length må ikke være længere end dna-strengens længde

    def clean_dna(self):
        """ DNA string should only consist of A, C, T and G's """
        dna = self.cleaned_data['dna'].lower()
        for letter in dna:
            if not letter in "actg": 
                raise forms.ValidationError(
                    'DNA-strengen må kun indeholde bogstaverne A, C, G og T.')
        if len(dna)<5:
            raise forms.ValidationError(
                'Din DNA-streng er for kort.')
        return dna

    def clean(self):
        """ 
        Form validation that depends on more than one input value. 
        Error message will be shown on top of the form. 
        """
        cleaned_data = super().clean()
        length = cleaned_data.get("length")
        start = cleaned_data.get("start")
        dna = cleaned_data.get("dna")

        if length and start and dna:

           if start + length > len(dna) + 1:
                raise forms.ValidationError(
                    "DNA-strengen er for kort til dine valg for primeren")
        
        return cleaned_data