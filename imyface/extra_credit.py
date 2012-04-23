import logging
from collections import deque
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import actions

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

def minimum_faces(user_id, face):
    """ find the shortest path between user_id->face, then return the length
    """
    return len(actions.find_path(user_id, face, find_shortest=True))

def _avg_path_length_for_user(user_id):
    all_users = _FACE_DATA.data.keys()
    path_lengths = [minimum_faces(user_id, u) for u in all_users]
    return sum(path_lengths) / len(path_lengths)

def degrees_of_separation(seps=None):
    all_users = _FACE_DATA.data.keys()
    seps = [_avg_path_length_for_user(u) for u in all_users]
    return sum(seps) / len(seps)
