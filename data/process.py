from concurrent.futures import process
from glob import glob
import csv

def process_sts_sem():
    files_from = glob('data/original/semeval-sts/**/*.tsv', recursive=True)
    print(files_from)
    cnt = 0
    prev_sent = 'I feel good today'
    with open('data/processed/sts_eval.csv', 'w') as fw:
        writer = csv.writer(fw)
        for file_path in files_from:
            print(file_path)
            with open(file_path, 'r') as fr:
                reader = csv.reader(fr, delimiter='\t' )
                for i, line in enumerate(reader):
                    try:
                        cnt += 1
                        data = [f'sts{cnt}', line[1], line[2], float(line[0])]
                        writer.writerow(data)

                        if i % 4 == 0:
                            data = [f'aug-{cnt}', line[1], line[1], 5.0]
                            writer.writerow(data)
                            data = [f'aug-{cnt}', line[1], prev_sent, 0.0]
                            writer.writerow(data)
                            prev_sent = line[1]

                    except:
                        print(line)

def process_sts_benchmark():
    # files_from = glob('data/original/stsbenchmark/**/*.csv', recursive=True)
    files_from = ['data/original/stsbenchmark/sts-dev.csv']
    print(files_from)
    with open('data/processed/val_sts_bn.csv', 'w') as fw:
        writer = csv.writer(fw)
        for file_path in files_from:
            print(file_path)
            with open(file_path, 'r') as fr:
                reader = csv.reader(fr, delimiter='\t' )
                for line in reader:
                    try:
                        cnt += 1
                        data = [f'stsb{cnt}', line[-1], line[-2], float(line[4])]
                        writer.writerow(data)
                    except:
                        print(line)
import json
def process_snli():
    files_from = glob('data/original/snli_1.0/**/*.jsonl', recursive=True)
    print(files_from)
    cnt = 0
    with open('data/processed/snli.csv', 'w') as fw:
        writer = csv.writer(fw)
        for file_path in files_from:
            with open(file_path, 'r') as fr:
                for json_str in fr:
                    data = json.loads(json_str)
                    line = [f'snli-{cnt}', data['sentence1'], data['sentence2'], tuple(data['annotator_labels'])]
                    cnt += 1
                    writer.writerow(line)


def generate_random():
    import random
    noun = ['apple', 'grape', 'school', 'korea', 'sentence', 'game', 'fighting', 'tree', 'flower', 'book', 'studying',
    'example', 'girl', 'body']
    sub = ['i', 'I', 'You', 'She', 'He']
    pos =  ['#sub want #noun', '#sub like #noun', '#sub hope #noun', '#sub love #noun', '#sub am in love with #noun']
    neg = ['#sub hate #noun', '#sub don\'t like #noun', '#sub dislike #noun', '#sub am not in love with #noun', '#sub does not hope #noun', '#sub do not like #noun']
    holder = []
    pos = list(map(lambda x: (x, 'pos'), pos))
    neg = list(map(lambda x: (x, 'neg'), neg))
    cand = pos + neg
    holder = set([])
    for i in range(50000):
        pickn = random.choice(noun)
        picks = random.choice(sub)
        sents = random.sample(cand, 2)
        score = 5 if sents[0][1] == sents[1][1] else 0
        to_add = [sents[0][0], sents[1][0]]
        to_add.sort()
        to_add.append(str(score))
        hs = '|'.join(to_add).replace('#sub', picks).replace('#noun', pickn)
        holder.add(hs)

    with open('data/processed/generated.csv', 'w') as fr:
        writer = csv.writer(fr)
        for item in holder:
            sent1, sent2, score = item.split('|')
            if float(score) > 2.5:
                label = ['entailment']
            else: 
                label = ['contradiction']

            writer.writerow(['generated', sent1, sent2, tuple(label)])

def combine_and_shuffle():
    import random
    files_from = glob('data/processed/**/*.csv', recursive=True)
    print(files_from)
    holder = []
    for path in files_from:
        with open(path, 'r') as fr:
            reader = csv.reader(fr)
            for line in reader:
                holder.append(line)
    random.shuffle(holder)
    with open('data/train.csv', 'w') as fw:
        writer = csv.writer(fw)
        for line in holder:
            writer.writerow(line)


if __name__ == '__main__':
    process_sts_sem()