import os
import shutil
import pandas as pd




class Instance(object):
    def __init__(self):
        pass

class Vocabulary(object):
    def __init__(self):
        pass


class Process_pipe(object):
    """
    parent class for process pip line
    """
    def __init__(self,raw_root, middle_root, processed_root):
        self.raw_root = raw_root
        self.middle_root = middle_root
        self.middle_folders = ['r2d',]
        self.middle_r2d_root = self.middle_root + 'r2d.json'
        self.processed_root = processed_root
        self.datasets = ['trainset', 'devset', 'testset']
        self.init_folders()
        self.df = pd.DataFrame()
        self.column_names = {''}
        self.features = {'seg', 'pos'}

    def init_folders(self):
        """
        mkdir folders like
        :return:
        """
        if os.path.exists(self.middle_root):
            shutil.rmtree(self.middle_root)
        if os.path.exists(self.processed_root):
            shutil.rmtree(self.processed_root)
        os.mkdir(self.middle_root)
        for middle in self.middle_r2d_root:
            os.mkdir(self.middle_root+middle)
        os.mkdir(self.processed_root)
        for dataset in self.datasets:
            os.mkdir(self.processed_root+dataset+'/')


    def raw_to_df(self, reading2df):
        """
        process raw to df
        if split
        save to middle
        df : pandas
        """
        file = os.listdir()
        df = reading2df()
        df.to_json(self.middle_r2d_root)





