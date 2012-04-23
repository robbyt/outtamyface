import logging
from collections import deque
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import actions

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

def minimum_faces(user_id, face):
    """ find the shortest path between user_id->face, then return the length
    """
    return len(actions.path_finder(user_id, face, find_shortest=True))
