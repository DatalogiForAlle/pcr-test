from django import forms


class DNAForm(forms.Form):

    upper_dna = forms.CharField(label="Øvre DNA-streng", initial="",
                          help_text="Indtast den øvre del af DNA-strengen")

    def clean_upper_dna(self):
        """ 
        DNA string should only consist of A, C, T and G's 
        Length of DNA should be at least 5.
        """
        upper_dna = self.cleaned_data['upper_dna'].lower()
        for letter in upper_dna:
            if not letter in "actg":
                raise forms.ValidationError(
                    'DNA-strengen må kun indeholde bogstaverne A, C, G og T.')
        if len(upper_dna) < 5:
            raise forms.ValidationError(
                'Din DNA-streng er for kort.')
        return upper_dna


class ForwardPrimerForm(forms.Form):
    
    start = forms.IntegerField(label="Primer start",
                               help_text="Ved hvilken baseposition (talt fra venstre) skal din primer begynde? Angiv et heltal på mindst 1.",
                               min_value=1
                               )
    length = forms.IntegerField(label="Primer længde", min_value=5,
                               help_text="Hvor mange baser skal din forward primer bestå af? Angiv et heltal på mindst 5.")

    def __init__(self, dna_length, *args, **kwargs):
        super(ForwardPrimerForm, self).__init__(*args, **kwargs)
        self.dna_length = dna_length

    def clean(self):
        """ 
        Form validation that depends on more than one input value. 
        Error message will be shown on top of the form. 
        """
        cleaned_data = super().clean()
        length = cleaned_data.get("start")
        start = cleaned_data.get("length")

        if length and start:

            if start + length > self.dna_length + 1:
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
