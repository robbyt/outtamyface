import logging
from collections import deque
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import actions

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

def minimum_faces(user_id, face):
    """ find the shortest path between user_id->face, then return the length
    """
    path = actions.find_path(user_id, face, find_shortest=True)
    if path:
        return len(path)
    else:
        return

def _avg_path_length_for_user(user_id):
    all_users = _FACE_DATA.data.keys()
    path_lengths = []
    for u in all_users:
        print "working on: " + str(u)
        mf = minimum_faces(user_id, u)
        if mf:
            path_lengths.append(mf)

    return sum(path_lengths) / len(path_lengths)

def degrees_of_separation(seps=None):
    assert(False)
    all_users = _FACE_DATA.data.keys()
    seps = [_avg_path_length_for_user(u) for u in all_users]
    return sum(seps) / len(seps)
