from collections import Counter


class Vocabulary_base(object):
    def __init__(self, feature_name_space):
        self.feature_name_space = feature_name_space

    def init_token2id(self):
        pass

    def load_pretrained_word2vec(self, path):
        raise NotImplementedError


class Vocabulary(Vocabulary_base):
    def __init__(self):
        pass


