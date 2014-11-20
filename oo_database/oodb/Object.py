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
                self.print_dict()
                raise err

        if inspect.ismethod(a):
            #logging.info('method', a())
            return a()
        else:
            #logging.info('not method')
            return a

    def has(self, name):
        if name in self.data:
            return True
        
        return hasattr(self, name)

    def pod_to_data(self):
        d = dict(self.__dict__)
        for k,v in d.items():
            if isinstance(v, str):
                print("str",k,v)
                self.data[k] = v
                delattr(self, k)


