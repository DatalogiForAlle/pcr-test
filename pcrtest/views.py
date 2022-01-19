from django.shortcuts import render, redirect
from .forms import DNAForm, ForwardPrimerForm, ReversePrimerForm
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
    """ Helper function that returns DNA-inverse string of input DNA """
    result = ""
    for c in some_string:
        result += INVERSE_BASE[c]
    return result


def primer_dimer(primer):
    """ 
    Input: A primer (string)
    Returns True if the primer can bind to itself. False otherwise. 
    """
    #reversed_primer = primer[::-1] 
    # for i in range(5, len(primer)):
    #     tail_of_primer = primer[-i:]
    #     head_of_reversed = reversed_primer[:i]
    #     inverse_head_of_reversed = inverse_string(head_of_reversed)
    #     if tail_of_primer == inverse_head_of_reversed:
    #         return True

    return False


def hetero_dimer(forward_primer, reverse_primer):
    """ 
    Return True if the two primers can bind to each other. 
    """
    return False


def clear_session_helper(request):
    """ Helper function that clears all session variables """

    for var in [
        'upper_dna', 
        'forward_primer_length', 
        'reverse_primer_length', 
        'reverse_primer_start',
        'forward_primer_start', 
        'forward_primer_is_good',
        'forward_primer'
    ]:
        if var in request.session:
            del request.session[var]

def clear_session(request):
    clear_session_helper(request)
    return redirect(reverse('forward-primer'))

def dna_input(request):

    if 'upper_dna' in request.session:
        form = DNAForm(
            initial={
                'upper_dna': request.session['upper_dna'].upper(), 
        })
    else:
        form = DNAForm()

    if request.method == 'POST':

        clear_session_helper(request)

        form = DNAForm(request.POST)
        if form.is_valid():
            request.session['upper_dna'] = form.cleaned_data['upper_dna'].lower()
            return redirect(reverse('forward-primer'))

    context = {'form': form}

    return render(request, "pcrtest/dna_input.html", context)


def forward_primer(request):
    if not 'upper_dna' in request.session:
        return redirect(reverse('dna-input'))
    
    upper_dna = request.session['upper_dna'].lower()
    dna_length = len(upper_dna)
    
    if 'forward_primer_start' in request.session:
        form = ForwardPrimerForm(dna_length,
            initial={
                'start':request.session['forward_primer_start'],
                'length':request.session['forward_primer_length']
                })
    else:
        form = ForwardPrimerForm(len(upper_dna))

    context = {}
    context['upper_dna'] = upper_dna
    context['lower_dna'] = inverse_string(upper_dna)
    context['forward_primer_to_show'] = "-" * dna_length
    
    if request.method == 'POST':

        form = ForwardPrimerForm(len(upper_dna), request.POST)
        if form.is_valid():
            primer_start = form.cleaned_data['start'] - 1
            primer_length = form.cleaned_data['length']

            primer = upper_dna[primer_start: primer_start + primer_length]
        
            # Make the primer string to be shown on page
            context['forward_primer_to_show'] = " " * primer_start + primer + \
                " " * (len(upper_dna) - primer_start - primer_length)
          
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
            context['tail_count'] = tail_count

            # Calculate number of places the primer fits the lower DNA-string
            context['occurences'] = count_substring(upper_dna, primer)

            # Check for if the primer cant bind to itself
            context['primer_dimer_condition'] = not primer_dimer(primer)
            
            # Does primer satisfy all criteria?
            primer_is_good = (context['occurences'] == 1) and context['primer_tail_condition'] and context['good_melting_point'] and context['primer_dimer_condition'] 
            
            # Store session variables
            request.session['forward_primer_is_good'] = primer_is_good
            request.session['forward_primer_start'] = form.cleaned_data['start']
            request.session['forward_primer_length'] = form.cleaned_data['length']
            request.session['forward_primer'] = primer
            context['show_results'] = True
            
    context['form'] = form

    return render(request, "pcrtest/forward.html", context)

@require_GET
def reverse_primer(request):
    if not 'forward_primer_is_good' in request.session:
        return HttpResponseRedirect(reverse('forward-primer'))
    if not request.session['forward_primer_is_good']:
        return HttpResponseRedirect(reverse('forward-primer'))
        
    forward_primer_start = int(request.session['forward_primer_start']) - 1 
    forward_primer_length = int(request.session['forward_primer_length'])
    upper_dna = request.session['upper_dna']
    dna_length = len(upper_dna)

    lower_dna = inverse_string(upper_dna)
    reverse_primer_to_show = "-" * dna_length
    f_primer = upper_dna[forward_primer_start: forward_primer_start + forward_primer_length]
    forward_primer_to_show = " " * forward_primer_start + f_primer + \
        " " * (len(upper_dna) - forward_primer_start - forward_primer_length)

    if 'reverse_primer_start' in request.session:
        form = ReversePrimerForm(len(upper_dna),
            initial={
                'reverse_primer_start': request.session['reverse_primer_start'],
                'reverse_primer_length': request.session['reverse_primer_length']
            })
    else:
        form = ReversePrimerForm(len(upper_dna))

    context = {
        'upper_dna':upper_dna,
        'lower_dna':lower_dna,
        'forward_primer_to_show':forward_primer_to_show,
        'counter': range(1, len(upper_dna) + 1)[::-1]
        }

    if 'reverse_primer_start' in request.GET:
        form = ReversePrimerForm(len(upper_dna), request.GET)

        request.session['reverse_primer_start'] = request.GET['reverse_primer_start']
        request.session['reverse_primer_length'] = request.GET['reverse_primer_length']

        if form.is_valid():
        
            reverse_primer_start = int(
                request.GET['reverse_primer_start']) - 1
            reverse_primer_length = int(request.GET['reverse_primer_length'])

            reverse_primer_start_from_left = len(upper_dna) - reverse_primer_start - reverse_primer_length
            reverse_primer_end_from_left = len(upper_dna) - reverse_primer_start 
            reverse_primer = inverse_string(upper_dna[reverse_primer_start_from_left:reverse_primer_end_from_left]) 

            context['reverse_primer'] = reverse_primer   
            reverse_primer_to_show = " " * reverse_primer_start_from_left + reverse_primer + \
                " " * (len(upper_dna) - reverse_primer_end_from_left)

            # Calculation of the reverse primer's melting point
            num_c = reverse_primer.count('c')
            num_g = reverse_primer.count('g')
            reverse_primer_melting_point = round(
                64.9 + 41*(num_c + num_g)/reverse_primer_length - 41*16.4/reverse_primer_length, 1)
            context['melting_point'] = reverse_primer_melting_point
            context['good_melting_point'] = 52 <= reverse_primer_melting_point <= 58

            # Either 2 or 3 of the last three bases in the primer has to be either C or G
            reverse_primer_tail = reverse_primer[:5]
            tail_count = reverse_primer_tail.count('c') + reverse_primer_tail.count('g')
            context['primer_tail_condition'] = 2 <= tail_count <= 3
            context['tail_count'] = tail_count

            # Calculate number of places the primer fits the lower DNA-string
            context['occurences'] = count_substring(lower_dna, reverse_primer)

            # Check if the primer cant bind to itself
            context['primer_dimer_condition'] = not primer_dimer(reverse_primer)
            
            # Check if the primer can bind to the reverse primer
            context['hetero_dimer_condition'] = not hetero_dimer(request.session['forward_primer'], 
                reverse_primer)

            # Does primer satisfy all criteria?
            context["reverse_primer_is_good"] = (
                context['occurences'] == 1) and context['primer_tail_condition'] and context['good_melting_point'] and context['hetero_dimer_condition']


    context['reverse_primer_to_show'] = reverse_primer_to_show

    context['form'] = form
    return render(request, "pcrtest/reverse.html", context)
