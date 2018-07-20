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


class Datas(object):
    def __init__(self):
        self.texts = []
        self.segs = []
        self.poss = []
        self.dataframe = pd.DataFrame()

    def get_instance(self, input):
        if input != '\n':
            lines = inputs.split('。')
            for line in lines:
                text = str.strip(line) + '。'
                self.texts.append(text)
                seg, pos = segment(text)
                self.segs.append(seg)
                self.poss.append(pos)

    def get_dataframe(self):
        df = pd.DataFrame({'text': self.texts, 'seg': self.segs, 'pos': self.poss})
        return df


class Preprocessor(object):
    def __init__(self, test=True):
        self.middle_path = 'raw/middle/'
        if test:
            self.file_list = ['raw/sample', 'raw/sample']
        else:
            self.file_list = ['raw/wiki_00', 'raw/wiki_01']

        self.vocab = Vocab()
        self.datas = Datas()

    def preprocess(self):
        if os.path.exists(self.middle_path):
            shutil.rmtree(self.middle_path)
        os.mkdir(self.middle_path)
        #texts, segs, poss = [], [], []

        for file in self.file_list:
            with open(file) as reader:
                for line in tqdm(reader, desc='get_corpus'):
                    self.datas.get_instance(line)

        df = self.datas.get_dataframe()
        df = df[df.seg.apply(len) > 6]
        df.to_json(self.middle_path + 'middle.json')
        print(f'middle file saved to {self.middle_path}')

    def build_vocab(self):
        self.vocab.build_vocab()

    def data_pipeline(self, inputs):
        """
        :param inputs: list of string
        :return:
        """
        self.datas = Datas()
        for i in inputs:
            pass




    def pipline(self):
        self.preprocess()
        self.build_vocab()
        print('done')

