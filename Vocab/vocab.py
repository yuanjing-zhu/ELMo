from collections import Counter
import pandas as pd
import os
import gensim
from tqdm import tqdm
import pickle as pk
import numpy as np
import shutil




class Vocab(object):

    def __init__(self):
        self.middle_path = 'raw/middle/middle.json'
        self.processed_df_path = 'processed_df/'
        self.fast_read_w2v = 'raw/word2vec_file/sgns.wiki.fastreading.m'
        self.token2ids = {'seg': {'<PAD>':0, '<UNK>':1}, 'pos': {'<PAD>':0, '<UNK>':1}}


    def build_vocab(self):
        self.df = pd.read_json(self.middle_path)
        self._get_counters()
        self.pipeline_gen_w2v()
        self._gen_converted_df()

    def _get_counters(self):

        self.counters = {'seg': Counter(), 'pos': Counter()}
        for i in zip(self.df.seg.apply(Counter), self.df.pos.apply(Counter)):
            self.counters['seg'].update(i[0])
            self.counters['pos'].update(i[1])


    def pipeline_gen_w2v(self, drop_old_fast_read=False):

        if drop_old_fast_read:
            os.remove(self.fast_read_w2v)

        if not os.path.exists(self.fast_read_w2v):
            print('load raw w2v file and gen fast_read_w2v')
            model = gensim.models.KeyedVectors.load_word2vec_format('raw/word2vec_file/sgns.wiki.bigram')
            dic_model = {}
            for i in model.index2word:
                dic_model[i] = model[i]
            pk.dump(dic_model, open(self.fast_read_w2v, 'wb'))
        else:
            print('using fast_read_w2v')
            model = pk.load(open(self.fast_read_w2v, 'rb'))

        count_in, count_notin = 0, 0
        bounds = np.random.uniform(-1, 1, 300).tolist()
        matrix = [np.zeros(300).tolist()] + [bounds]
        for index, word in tqdm(enumerate(self.counters['seg']), desc='rebuild embedding matrix'):
            try:
                matrix.append(model[word].tolist())
                self.token2ids['seg'][word] = index + 2
                count_in += 1
            except:
                count_notin += 1
        print(f'{count_in} in found')
        print(f'{count_notin} not found')

    def seg_list_token2id(self, input_list):
        res = [self.token2ids['seg'][i] if i in self.token2ids['seg'] else 1 for i in input_list]
        return res

    def pos_list_token2id(self, input_list):
        res = [self.token2ids['pos'][i] if i in self.token2ids['pos'] else 1 for i in input_list]
        return res


    def _gen_converted_df(self):
        if os.path.exists(self.processed_df_path):
            shutil.rmtree(self.processed_df_path)
        os.mkdir(self.processed_df_path)

        self.df['seg_ids'] = self.df.seg.apply(self.seg_list_token2id)
        self.df['pos_ids'] = self.df.pos.apply(self.pos_list_token2id)
        self.df.to_json(self.processed_df_path+'processed_df.json')
        print(f'converted to id and saved to {self.processed_df_path}')


    def save(self):
        name = 'Vocab/vocab.pkl'
        pk.dump(self, open(name, 'wb'))
        print(f'vocab saved to {name}')
