import logging
import inspect

import oodb



class Object:
    def __init__(self, i):
        self.id = i
        self.data = {}

    def print_dict(self):
        logging.info('__dict__:')
        for k,v in self.__dict__.items():
            logging.info("{} {}".format(k,v))

    def get(self, name):
        #logging.info('get')

        try:
            a = self.data[name]
        except:
            try:
                a = getattr(self, name)
            except AttributeError as err:
                raise err

        if inspect.ismethod(a):
            #logging.info('method', a())
            return a()
        else:
            #logging.info('not method')
            return a

    def has(self, name):
        return hasattr(self, name)

