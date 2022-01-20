TOTAL_MATCH_LIMIT = 10
CONSECUTIVE_MATCH_LIMIT = 5


INVERSE_BASE = {
    'a': 't',
    't': 'a',
    'c': 'g',
    'g': 'c',
    'x': 'x'
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

def count_matches(seq1, seq2):
    count = 0
    for idx, char in enumerate(seq1):
        if char == INVERSE_BASE[seq2[idx]]:
            count += 1
    return count


def determine_longest_consecutive_match(seq1, seq2):
    """
    Helper functions that determines the length of the longest consecutive match in two strings of equal length
    Examples
    seq1 = "abe1234gås"
    seq2 = "gås1234abe"
    should return 4
    
    seq1 = "be1234gåsa"
    seq2 = "gås1234abe"
    should return 0
    
    """
    seq1 = seq1.lower()
    seq2 = seq2.lower()
    assert len(seq1) == len(seq2) 

    max = 0
    for i in range(len(seq1)+1):
        max_i = 0
        for j in range(i, len(seq1)+1):
            substr1 = seq1[i:j]
            substr2 = seq2[i:j]
            
            if substr1 == substr2:
                if len(substr1) > max_i:
                    max_i = len(substr1)
                    # If we get performance issues, we can cut the search of here:
                    #if max_i > CONSECUTIVE_MATCH_LIMIT:
                    #    return max_i
        if max_i > max:
            max = max_i
    return max


def check_for_dimers(primer1, primer2):
    """ 
    Helper function to check for primer-dimer and hetero-dimer
    Should return True if the primers bind to each other. False otherwise. 
    """
    primer1 = primer1.lower()
    primer2 = primer2.lower()

    
    # Check for matches in overlap (part 1)
    for i in range(1, len(primer1) + 1):
        # Let's say that the primer is 12345
        # Then the priver_reverse is 54321
        # In this loop we explore the matches in the overlaps below:
        # 12345
        # ----------
        #     54321
        #    54321
        #   54321
        #  54321
        # 54321

        overlap_primer = primer1[-i:]
        overlap_reverse = primer2[:i]
        
        total_matches_in_overlap = count_matches(overlap_primer, overlap_reverse)
        if total_matches_in_overlap > TOTAL_MATCH_LIMIT:
            print("Total match too big (1):",
                  total_matches_in_overlap, overlap_primer, overlap_reverse)

            return True

        longest_consecutive_match = determine_longest_consecutive_match(overlap_primer, inverse_string(overlap_reverse))
        if longest_consecutive_match > CONSECUTIVE_MATCH_LIMIT:
            print("Consecutive match to big (2)",
                  longest_consecutive_match, overlap_primer, overlap_reverse)
            return True
            
    for i in range(1, len(primer1)):
        # Check for total matches in overlap (part 2)
        # In this loop we explore the matches in the overlaps below:
        #     12345
        # ----------
        # 54321
        #  54321
        #   54321
        #    54321

        overlap_primer = primer1[:i]
        overlap_reverse = primer2[-i:]


        total_matches_in_overlap = count_matches(
            overlap_primer, overlap_reverse)
        if total_matches_in_overlap > TOTAL_MATCH_LIMIT:
            print("Total match too big (2):", total_matches_in_overlap, overlap_primer, overlap_reverse)

            return True
        
        longest_consecutive_match = determine_longest_consecutive_match(
            overlap_primer, inverse_string(overlap_reverse))
        if longest_consecutive_match > CONSECUTIVE_MATCH_LIMIT:
            print("Consecutive match to big (2)", longest_consecutive_match, overlap_primer, overlap_reverse)

            return True

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


if __name__ == "__main__":
    primer = "aaatttxxx"
    print(not check_for_dimers(primer, primer[::-1]))
    

