from django import forms

class PrimerForm(forms.Form):
    
    dna = forms.CharField(max_length=300, label="DNA-streng", initial="TGGCCTGTGGGTCCCCCCATAGATCATAAGCCCAGGAGGAAGGGCTGTGTTTCAGGGCTGTGATCACTAGCACCCAGAACCGTCGACTGGCACAGAACAGGCACTTAGGGAACCCTCACTGAATGAATGAATGAATGAATGAATGAATGAATGTTTGGGCAAATAAACGCTGACAAGGACAGAAGGGCCTAGCGGGAAGGG",
                                    help_text="Indtast DNA-streng")

    start = forms.IntegerField(label="Primer start",
                               help_text="Hvor mange bogstaver fra venstre skal din primer begynde? Angiv et heltal mellem 0 og DNA-strengens længde.",
                               min_value=0
                               )

    length = forms.IntegerField(label="Primer længde", min_value=5,
                               help_text="Hvor mange baser skal din primer bestå af? Angiv et heltal større end 4.")


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
        # Ensure start + length <= len(dna)
        cleaned_data = super().clean()
        length = cleaned_data.get("length")
        start = cleaned_data.get("start")
        dna = cleaned_data.get("dna")

        if length and start and dna:

            if start > len(dna):
                raise forms.ValidationError(
                    f"Primerens startposition må ikke være større end DNA-strengens længde (={len(dna)})")

            if length > len(dna):
                raise forms.ValidationError(
                    f"Primerens startposition må ikke være større end DNA-strengens længde (={len(dna)})")

            if start + length > len(dna):
                raise forms.ValidationError(
                    "Summen af primerens startposition og længde må ikke være større en DNA-strengens længde")
        
        return cleaned_data