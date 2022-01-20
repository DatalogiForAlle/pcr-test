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


def calculate_melting_point(primer):
    """ Helper function to calculate melting point of primer """
    num_c = primer.count('c')
    num_g = primer.count('g')
    primer_length = len(primer)
    melting_point = round(
        64.9 + 41*(num_c + num_g)/primer_length - 41*16.4/primer_length, 1)

    return melting_point


def primer_dimer(primer):
    """ 
    Helper function to determine if primer has 'primer dimer' (can bind to itself)
    Input: A primer (string)
    Should return True if the primer can bind to itself. False otherwise. 
    """
    # Not implemented
    return False


def hetero_dimer(forward_primer, reverse_primer):
    """ 
    Helper function to determine if primers has 'hetero dimer' (can bind to each other)

    Both input values are strings.
    Should return True if the two primers can bind to each other. False otherwise 
    """
    # Not implemented
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
