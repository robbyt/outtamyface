import os
import persist

PERSIST_DATA = os.path.dirname(__file__) + '/face.pickle'
SAVE_EVERY = 3

try:
    FACE_DATA = persist.load(PERSIST_DATA)

except:
    FACE_DATA = {}


def save():
    global SAVE_EVERY

    if SAVE_EVERY <= 1:
        persist.save(FACE_DATA, PERSIST_DATA)
        SAVE_EVERY = 3
    else:
        SAVE_EVERY -= 1
