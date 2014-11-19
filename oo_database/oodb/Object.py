import logging
import inspect

import oodb

class Object:

    def print_dict(self):
        logging.info('__dict__:')
        for k,v in self.__dict__.items():
            logging.info("{} {}".format(k,v))

    def get(self, name):
        #logging.info('get')

        try:
            a = getattr(self, name)
        except AttributeError as err:
            raise err
            return None

        

        if inspect.ismethod(a):
            #logging.info('method', a())
            return a()
        else:
            #logging.info('not method')
            return a

    def objects(self):
        for o in oodb.DB.objects():
            if isinstance(o, type(self)):
                yield o


