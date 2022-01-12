from django.shortcuts import render
from .forms import PrimerForm

INVERSE_BASE = {
    'a': 't',
    't': 'a',
    'c': 'g',
    'g': 'c'
}

def count_substring(string, str_to_search_for):
    """ Returns the number of occurences of substring in string (with overlaps) """
    count = 0
    for x in range(len(string) - len(str_to_search_for) + 1):
        if string[x:x+len(str_to_search_for)] == str_to_search_for:
            count += 1
    return count


def inverse_string(some_string):
    result = ""
    for c in some_string:
        result += INVERSE_BASE[c]
    return result

def home(request):

    form = PrimerForm
    context = {}
    context["range"] = range(36)

    if request.method == 'POST':
        form = PrimerForm(request.POST)
        if form.is_valid():
            dna = form.cleaned_data['dna'].lower()
            primer_start = form.cleaned_data['start'] - 1
            primer_length = form.cleaned_data['length']

            primer = dna[primer_start: primer_start + primer_length]
            context['lower_dna'] = inverse_string(dna)

            # Calculation of melting point
            num_c = primer.count('c')
            num_g = primer.count('g') 
            primer_melting_point = round(64.9 + 41*(num_c + num_g)/primer_length - 41*16.4/primer_length, 1)
            context['melting_point'] = primer_melting_point
            context['good_melting_point'] = 52 <= primer_melting_point <= 58

            # Make primer string to be shown on page    
            context['primer'] = " " * primer_start + primer + " " * (len(dna) - primer_start - primer_length) 

            # 2 or 3 of the last three bases in the primer has to be either C or G
            primer_tail = primer[-5:]
            tail_count = primer_tail.count('c') + primer_tail.count('g')
            context['primer_tail_condition'] = 2 <= tail_count <= 3

            # calculate number of places the primer fits the lower DNA-string
            context['occurences'] = count_substring(dna, primer)

    context['form'] = form


    return render(request, "pcrtest/home.html", context)
