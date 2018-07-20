import os
import shutil
from instance import Instance
import json
from tqdm import tqdm
from decorator import timer
from vocabulary import Vocabulary_base


class Handler_base(object):
    """
    usage: inherit the base class and take the implement of the funcations: raw2middle,
    init_feature_column_list, preprocess_func
    """
    def __init__(self, raw_folder, middle_folder, processed_folder):
        self.raw_folder = raw_folder
        self.middle_folder = middle_folder
        self.processed_folder = processed_folder
        self.instance_collector = []
        self.init_folder()

    @timer
    def init_folder(self):
        if os.path.exists(self.middle_folder):
            shutil.rmtree(self.middle_folder)
        if os.path.exists(self.processed_folder):
            shutil.rmtree(self.processed_folder)
        os.mkdir(self.middle_folder)
        os.mkdir(self.processed_folder)

    def gen_vocabulary(self):
        pass

    def handle_file(self, raw_file, prefix):
        """
        :param raw_file:
        :return:
        """
        ## raw to middle
        middle_data = self.raw2middle(self.raw_folder + raw_file)
        middle_file_name = self.middle_folder + str(prefix) + '.json'
        with open(middle_file_name, 'w') as writer:
            for line in middle_data:
                json.dump(line, writer)
                writer.write('\n')
        ## middle to middle1 ()
        self.loop_middle_gen_middle1(prefix)
        ## middle1 to processed

    @timer
    def raw2middle(self, raw_file):
        """
        raw_file : path to a raw file
        :return: list of dict
        self.middle1 = path
        """
        raise NotImplementedError

    @timer
    def loop_middle_gen_middle1(self, prefix):
        with open(self.middle_folder + prefix + '.json') as reader, open(self.middle_folder + prefix + '_1.json', 'w') as writer:
            for line_str in tqdm(reader, desc='gen_instances'):
                line_dict = json.loads(line_str)
                instance = self.gen_instance(line_dict)
                instance.check()
                json.dump(instance.data, writer)
                writer.write('\n')

    @timer
    def loop_middle1_gen_processed(self, prefix):
        # gen vocab, convert to id , save to processed
        pass


    def gen_instance(self, line_dict):
        """
        column1 = Column()
        column1.take_in_data(line_dict['sdf'])
        column2 = Column()
        column2.take_in_data(line_dict['dfd'])
        columns = [column1, column2]

        instance = Instance(columns)
        instance.check()
        :param line_dict:
        :return: instance.data
        """

        raise NotImplementedError

    def gen_vocabulary(self):
        pass

