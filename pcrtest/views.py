from django.shortcuts import render
from .forms import PrimerForm

inverse = {
    'a': 't', 
    't':'a', 
    'c': 'g',
    'g':'c'
}


def count_substring(string, str_to_search_for):
    count = 0
    for x in range(len(string) - len(str_to_search_for) + 1):
        if string[x:x+len(str_to_search_for)] == str_to_search_for:
            count += 1
    return count

def inverse_string(some_string):
    result = ""
    for c in some_string:
        result += inverse[c]
    return result

def home(request):

    form = PrimerForm
    context = {}
    context["range"] = range(36)

    if request.method == 'POST':
        form = PrimerForm(request.POST)
        if form.is_valid():
            dna = form.cleaned_data['dna'].lower()
            primer_start = form.cleaned_data['start']
            primer_length = form.cleaned_data['length']
            context['dna'] = dna

            dna_segment = dna[primer_start:primer_start+primer_length]
            primer = inverse_string(dna_segment)
            
            # Calculation of melting point
            num_c = primer.count('c')
            num_g = primer.count('g') 
            primer_melting_point = round(64.9 + 41*(num_c + num_g)/primer_length - 41*16.4/primer_length, 1)
            context['melting_point'] = primer_melting_point
            context['good_melting_point'] = 52 <= primer_melting_point <= 58


            # Make primer list to be shown on page
            primer_list = []
            for idx, char in enumerate(dna):
                if primer_start <= idx < primer_start + primer_length:
                    primer_list.append(inverse[char])
                else:
                    primer_list.append("") 
            context['primer'] = primer_list

            # 2 or 3 of the last three bases in the primer has to be either C or G
            primer_tail = primer[-5:]
            tail_count = primer_tail.count('c') + primer_tail.count('g')
            context['primer_tail_condition'] = 2 <= tail_count <= 3

            # check if primer only fits the DNA-string at one position
            context['occurences'] = count_substring(dna, dna_segment)

    context['form'] = form


    return render(request, "pcrtest/home.html", context)
