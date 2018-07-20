import pandas as pd
from tqdm import tqdm
import os
import shutil
import pyhanlp
import re
from Vocab import Vocab


def clean(input):
    res = re.sub(r'[()\'「」（）“”"]', '', input)
    return res


def segment(input):
    input = clean(input)
    input = list(pyhanlp.HanLP.segment(input))
    seg = [i.toString().split('/')[0] for i in input]
    pos = [i.toString().split('/')[1] for i in input]
    return seg, pos


def preprocess(test=False):

    middle_path = 'raw/middle/'
    if os.path.exists(middle_path):
        shutil.rmtree(middle_path)
    os.mkdir(middle_path)
    if test:
        file_list = ['raw/sample', 'raw/sample']
    else:
        file_list = ['raw/wiki_00', 'raw/wiki_01']

    texts = []
    segs = []
    poss = []
    for file in file_list:
        with open(file) as reader:
            for line in tqdm(reader, desc='get_corpus'):
                if line != '\n':
                    lines = line.split('。')

                    for i in lines:

                        if (i != '\n') & (i != ''):
                            text = str.strip(i)+'。'
                            texts.append(text)
                            seg, pos = segment(text)
                            segs.append(seg)
                            poss.append(pos)

    df = pd.DataFrame({'text': texts, 'seg': segs, 'pos': poss})
    df = df[df.seg.apply(len) > 6]
    df.to_json(middle_path + 'middle.json')
    print(f'middle file saved to {middle_path}')


preprocess(test=True)
vocab = Vocab()
vocab.build_vocab()
vocab.save()


