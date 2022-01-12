from django.shortcuts import render
from .forms import ForwardPrimerForm, ReversePrimerForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

INVERSE_BASE = {
    'a': 't',
    't': 'a',
    'c': 'g',
    'g': 'c'
}

def count_substring(string, str_to_search_for):
    """ Returns the number of occurences of substring in string (with overlaps) """
    count = 0
    for i in range(len(string) - len(str_to_search_for) + 1):
        if string[i:i+len(str_to_search_for)] == str_to_search_for:
            count += 1
    return count

def inverse_string(some_string):
    result = ""
    for c in some_string:
        result += INVERSE_BASE[c]
    return result

def home(request):
    return HttpResponseRedirect(reverse('forward-primer'))

def forward_primer(request):

    form = ForwardPrimerForm
    context = {}
    context["range"] = range(36)

    if request.method == 'POST':
        form = ForwardPrimerForm(request.POST)
        if form.is_valid():
            dna = form.cleaned_data['dna'].lower()
            primer_start = form.cleaned_data['start'] - 1
            primer_length = form.cleaned_data['length']

            primer = dna[primer_start: primer_start + primer_length]
            context['upper_dna'] = dna
            context['lower_dna'] = inverse_string(dna)
        
           # Make the primer string to be shown on page
            context['forward_primer_to_show'] = " " * primer_start + primer + \
                " " * (len(dna) - primer_start - primer_length)

            # Calculation of the primer's melting point
            num_c = primer.count('c')
            num_g = primer.count('g') 
            primer_melting_point = round(64.9 + 41*(num_c + num_g)/primer_length - 41*16.4/primer_length, 1)
            context['melting_point'] = primer_melting_point
            context['good_melting_point'] = 52 <= primer_melting_point <= 58

            # Either 2 or 3 of the last three bases in the primer has to be either C or G
            primer_tail = primer[-5:]
            tail_count = primer_tail.count('c') + primer_tail.count('g')
            context['primer_tail_condition'] = 2 <= tail_count <= 3

            # Calculate number of places the primer fits the lower DNA-string
            context['occurences'] = count_substring(dna, primer)

            # Does primer satisfy all criteria?
            context['primer_is_good'] = (context['occurences'] == 1) and context['primer_tail_condition'] and context['good_melting_point']  

            # Additional info we need
            context['forward_primer_start'] = form.cleaned_data['start']
            context['forward_primer_length'] = form.cleaned_data['length']

    context['form'] = form


    return render(request, "pcrtest/forward.html", context)


@require_POST
def reverse_primer(request):
    forward_primer_start = int(request.POST['forward_primer_start']) - 1 
    forward_primer_length = int(request.POST['forward_primer_length'])
    upper_dna = request.POST['upper_dna']
    lower_dna = inverse_string(upper_dna)
    reverse_primer_to_show = "-" * len(upper_dna)
    f_primer = upper_dna[forward_primer_start: forward_primer_start + forward_primer_length]
    forward_primer_to_show = " " * forward_primer_start + f_primer + \
        " " * (len(upper_dna) - forward_primer_start - forward_primer_length)
    form = ReversePrimerForm(len(upper_dna)) 
    context = {
        'upper_dna':upper_dna,
        'lower_dna':lower_dna,
        'forward_primer_to_show':forward_primer_to_show,
        'forward_primer_start': forward_primer_start,
        'forward_primer_length':forward_primer_length,
        'counter': range(1, len(upper_dna) + 1)[::-1]
        }

    if 'reverse_primer_start' in request.POST:
        form = ReversePrimerForm(len(upper_dna), request.POST)
        if form.is_valid():
            reverse_primer_start = int(
                request.POST['reverse_primer_start']) - 1
            reverse_primer_length = int(request.POST['reverse_primer_length'])

            reverse_primer_start_from_left = len(upper_dna) - reverse_primer_start - reverse_primer_length
            reverse_primer_end_from_left = len(upper_dna) - reverse_primer_start 
            reverse_primer = inverse_string(upper_dna[reverse_primer_start_from_left:reverse_primer_end_from_left]) 

            context['reverse_primer'] = reverse_primer   
            reverse_primer_to_show = " " * reverse_primer_start_from_left + reverse_primer + \
                " " * (len(upper_dna) - reverse_primer_end_from_left)
           

    context['reverse_primer_to_show'] = reverse_primer_to_show

    context['form'] = form
    return render(request, "pcrtest/reverse.html", context)
