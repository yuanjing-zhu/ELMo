


class Column(object):

    def __init__(self, name):
        self.name = name
        self.data = {}

    def take_in_data(self, data):

        raise NotImplementedError

    def process_func(self, data):

        raise NotImplementedError

    def show_data_info(self):
        assert self.data != {}
        print(f'columns : {self.data.keys()}')
        print(f'features: {self.data[self.data.keys()[0]].keys()}')
        print(f'data: {self.data}')

