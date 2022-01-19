from django import forms

class ForwardPrimerForm(forms.Form):
    
    dna = forms.CharField(max_length=300, label="Øvre DNA-streng", initial="",
                                    help_text="Indtast den øvre del af DNA-streng")

    start = forms.IntegerField(label="Primer start",
                               help_text="Ved hvilken baseposition (talt fra venstre) skal din primer begynde? Angiv et heltal på mindst 1.",
                               min_value=1
                               )
    length = forms.IntegerField(label="Primer længde", min_value=5,
                               help_text="Hvor mange baser skal din forward primer bestå af? Angiv et heltal på mindst 5.")

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


class ReversePrimerForm(forms.Form):
    
    reverse_primer_start = forms.IntegerField(label="Reverse primer start",
                               help_text="Ved hvilken baseposition (talt fra højre) skal din primer begynde? Angiv et heltal på mindst 1.",
                               min_value=1)
    reverse_primer_length = forms.IntegerField(label="Reverse primer længde", 
                               help_text="Hvor mange baser skal din reverse primer bestå af? Angiv et heltal på mindst 5.",
                               min_value=5)

    def __init__(self, dna_length, *args, **kwargs):
        super(ReversePrimerForm, self).__init__(*args, **kwargs)
        self.dna_length = dna_length

    def clean(self):
        """ 
        Form validation that depends on more than one input value. 
        Error message will be shown on top of the form. 
        """
        cleaned_data = super().clean()
        length = cleaned_data.get("reverse_primer_length")
        start = cleaned_data.get("reverse_primer_start")

        if length and start:

           if start + length > self.dna_length + 1:
               raise forms.ValidationError(
                   "DNA-strengen er for kort til dine valg for primeren")

        return cleaned_data
