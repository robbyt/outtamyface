import os
import persist

PERSIST_DATA = os.path.dirname(__file__) + '/user_data.pickle'

SAVE_EVERY = 3

try:
    USER_DATA = persist.load(PERSIST_DATA)

except:
    USER_DATA = {}


def save():
    global SAVE_EVERY

    if SAVE_EVERY <= 1:
        persist.save(USER_DATA, PERSIST_DATA)
        SAVE_EVERY = 3
    else:
        SAVE_EVERY -= 1
