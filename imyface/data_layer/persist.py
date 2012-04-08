import os
import shutil
import tempfile
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.debug("Setup logging")

import cPickle as pickle
#import msgpack

PERSIST = False

class NotWorking(Exception):
    pass

def save(data_to_save, file_target):
    if PERSIST:
        raise NotWorking

        logging.debug("Saving file: " + file_target)
        tmp = tempfile.NamedTemporaryFile()
        pickle.dump(data_to_save, tmp, protocol=2)

        if os.path.isfile(file_target):
            logging.debug("Removing old data persistance file: " + file_target)
            os.remove(file_target)
        
        shutil.copyfile(tmp.name, file_target)
        tmp.close()
    else:
        return

def load(file_target):
    if PERSIST:

        if os.path.isfile(file_target):
            logging.debug("Loading file: " + file_target)
            fp = open(file_target, 'rb')
            data = pickle.load(fp)
            fp.close()

        else:
            logging.debug("Can not load data from file: " + file_target)
            data = None

        if data is None:
            logging.debug("Problem loading data, returning empty dict")
            return {}
        else:
            logging.debug("Returning your data")
            return data
    else:
        return {}

