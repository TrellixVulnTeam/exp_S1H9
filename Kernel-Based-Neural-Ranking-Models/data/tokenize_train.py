import re

word2ind = {}
f = open('vocab.tsv')

for line in f:
        line = line.strip('\n').split('\t')
        word2ind[line[0]] = line[1]

regex_drop_char = re.compile('[^a-z0-9\s]+')
regex_multi_space = re.compile('\s+')

def tokenize(s):
        lst = regex_multi_space.sub(' ', regex_drop_char.sub(' ', s.lower())).strip().split()
        lst = [word2ind[i] if i in word2ind else '0' for i in lst]
        return ','.join(lst)

f = open('/work/ececis_research/Manning/triples.train.small.tsv')
fout = open('/work/ececis_research/Manning/train1.txt', 'w')

for line in f:
        line = line.strip('\n').split('\t')
        line[0] = tokenize(line[0])
        line[1] = tokenize(line[1])
        line[2] = tokenize(line[2])
        fout.write('\t'.join(line) + '\n')
