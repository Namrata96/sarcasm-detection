#import re
#num_chars = []
#
#num_lines = 0
#
#with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic.txt") as f:
#    for idx, line in enumerate(f):
#        if idx == 0:
#            continue
#        num_chars.append(len(line) - 1)
#        num_lines += 1
#
#print "num_lines: " + str(num_lines)
#
## print str(num_chars)
#
#with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic_senti.txt") as f:
#    nonsarcastic = f.read().splitlines()
#
#print "num_lines: " + str(len(nonsarcastic))
#
#for idx, line in enumerate(nonsarcastic):
#    # print "Removing " + str(num_chars[idx]) + " characters out of " + str(len(line))
#    nonsarcastic[idx] = line[num_chars[idx] + 1:]
#
#with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/processed_nonsarcastic.txt", 'w') as f:
#    for line in nonsarcastic:
#        f.write(line + "\n")
#
#with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/processed_nonsarcastic.txt", 'r') as f:
#    w = open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic_clean.txt", 'w')
#    
#    lines = f.readlines()
#    for line in lines[:1]:
#        new_line = str()
#        print line
#        m = re.search('\[', line)
#        i = m.start()
#        for j in range(i, 0, -1):
#            if line[j] == " ":
#                new_line = line[j+1:]
#                new_line = re.sub('\[\[.*]]', '', new_line)
#                print new_line
#                break
##        line = re.sub('\[\[[a-z]*[A-Z]*[0-9]*[, ]*]]', '', line)
##        line = re.sub('<br>', '', line)
##        w.write(line+"\n")
#    w.close()

with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_nonsarcastic_senti.txt",'r') as f:
    nonsarcastic = f.read().splitlines()
 
print "num_lines: " + str(len(nonsarcastic))
 
for idx, line in enumerate(nonsarcastic):
    idx1 = line.find('[')
    while line[idx1] != ' ' and idx1 > 0:
        idx1 -= 1
 
    line = line[idx1+1:]
 
    idx1 = line.find('[[[')
    idx2 = line.find(']]]')
    if (idx1 != -1 and idx2 != -1):
        print "Removing chars from " + str(idx1) + " to " + str(idx2+3) + ": " + line[idx1:idx2+4]
        line = line[:idx1] + line[(idx2+4):]
    while line.find('[[') != -1:
    	idx1 = line.find('[[')
    	idx2 = line.find(']]')
        print "Removing chars from " + str(idx1) + " to " + str(idx2+2) + ": " + line[idx1:idx2+3]
    	line = line[:idx1] + line[(idx2+3):]
 
    nonsarcastic[idx] = line
 
 
with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/processed_nonsarcastic.txt", 'w') as f:
    for line in nonsarcastic:
        f.write(line + "\n")
        
with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/test_sarcastic_senti.txt",'r') as f:
    sarcastic = f.read().splitlines()
 
print "num_lines: " + str(len(sarcastic))
 
for idx, line in enumerate(sarcastic):
    idx1 = line.find('[')
    while line[idx1] != ' ' and idx1 > 0:
        idx1 -= 1
 
    line = line[idx1+1:]
 
    idx1 = line.find('[[[')
    idx2 = line.find(']]]')
    if (idx1 != -1 and idx2 != -1):
        print "Removing chars from " + str(idx1) + " to " + str(idx2+3) + ": " + line[idx1:idx2+4]
        line = line[:idx1] + line[(idx2+4):]
    while line.find('[[') != -1:
    	idx1 = line.find('[[')
    	idx2 = line.find(']]')
        print "Removing chars from " + str(idx1) + " to " + str(idx2+2) + ": " + line[idx1:idx2+3]
    	line = line[:idx1] + line[(idx2+3):]
 
    sarcastic[idx] = line
 
 
with open("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/processed_sarcastic.txt", 'w') as f:
    for line in sarcastic:
        f.write(line + "\n")