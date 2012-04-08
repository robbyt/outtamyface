import os
import shutil
import tempfile

import msgpack

PERSIST = True

def save(data_to_save, file_target):
    if PERSIST:
        tmp = tempfile.TemporaryFile()
        msgpack.dump(data_to_save, tmp)

        if os.path.isfile(file_target):
            os.remove(file_target)
        
        shutil.copyfile(tmp.name, file_target)
        tmp.close()
    else:
        return

def load(file_target):
    if PERSIST:
        fp = open(file_target, 'rb')
        data = msgpack.load(fp)
        fp.close()
        return data
    else:
        return {}

