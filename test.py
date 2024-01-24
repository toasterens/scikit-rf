# %%
a = "1, 2, 3"
a_int = int(a)
print(a_int)
print(type(a_int))

# %%

import re

my_string = "Scd_21"
substrings_to_check = ['dd', 'dc', 'cd', 'cc']

pattern = re.compile('|'.join(map(re.escape, substrings_to_check)), re.IGNORECASE)

result = bool(pattern.search(my_string))

print(result)

# %%

import re

parameter = "Scd_21"

bal_str = ['dd', 'dc', 'cd', 'cc']
pattern = re.compile('|'.join(map(re.escape, bal_str)), re.IGNORECASE)
res = bool(pattern.search(parameter))

print(result)