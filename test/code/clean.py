

import re
from pandas import read_csv
file_path = '/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic_senti.txt'
new_file_path = '/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic_clean.txt'
wp = open(new_file_path, 'w')
fp = open(file_path, 'r')

pandas_data = read_csv(file_path, delimiter='\t')
print pandas_data[0]
lines = fp.readlines()
for line in lines[:1]:
    print line
    m = re.search("\d", line)
    print m.start()