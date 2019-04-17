# Prompts the user for a positive integer that codes a set S as follows:
# - Bit 0 codes 0
# - Bit 1 codes -1
# - Bit 2 codes 1
# - Bit 3 codes -2
# - Bit 4 codes 2
# - Bit 5 codes -3
# - Bit 6 codes 3
# ...
# Computes a derived positive integer that codes the set of running sums
# ot the members of S when those are listed in increasing order.
#
# Written by *** and Eric Martin for COMP9021


from itertools import accumulate
import sys

try:
    encoded_set = int(input('Input a positive integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
	
	
def display_encoded_set(encoded_set):
    print('{', end='')
    print(', '.join(str(i) for i in encode(encoded_set)), end='')
    print('}')


def encode(encoded_set):
    result = []
    Twointeger = bin(encoded_set)[2:]
    Twointeger = list(Twointeger)
    Twointeger.reverse()
    for m in range(len(Twointeger)):
        if Twointeger[m] == '1':
            if m == 0:
                result.append(0)
            if m%2 == 0 and m != 0:
                result.append(int(m//2))
            if m%2 == 1:
                result.append(int(-(m+1)//2))
    return sorted(result, reverse = False)

def code_derived_set(encoded_set):
    encoded_running_sum = 0
    tmp = encode(encoded_set)
    derived_encoded_set = accumulate(tmp)
    derived_encoded_set = list(set(derived_encoded_set))
    for i in derived_encoded_set:
        if i >= 0:
            encoded_running_sum += pow(2, (i*2))
        if i < 0:
            encoded_running_sum += pow(2, (-(i*2)-1))  

    return encoded_running_sum

print('The encoded set is: ', end = '')
display_encoded_set(encoded_set)
encoded_running_sum = code_derived_set(encoded_set)
print('The derived encoded set is: ', end = '')
display_encoded_set(encoded_running_sum)
print('  It is encoded by:', encoded_running_sum)
    