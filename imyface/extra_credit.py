from multiprocessing import Process, Queue 

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import actions

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

def minimum_faces(user_id, face, q=None):
    """ find the shortest path between user_id->face, then return the length
    """
    path = actions.find_path(user_id, face, find_shortest=True)
    if path:
        if q is None:
            return len(path)

        else:
            # for multiprocessing
            q.put(len(path))
    else:
        return

def avg_path_length_for_user(user_id):
    """ This will take a really really long time to finish.
    """
    all_users = _FACE_DATA.data.keys()
    path_lengths = []
    for u in all_users:
        #logging.debug("working on: " + str(u))
        mf = minimum_faces(user_id, u)
        if mf:
            path_lengths.append(mf)

    return sum(path_lengths) / len(path_lengths)

def avg_path_length_for_user_mp(user_id):
    """ This will take a really long time / your number of CPUs
    """
    all_users = _FACE_DATA.data.keys()
    jobs = []
    q = Queue()

    for u in all_users:
        p = Process(target=minimum_faces, args=(user_id, u, q,))
        jobs.append(p)
        logging.debug("Starting job: " + str(p))
        p.start()

    for job in jobs:
        logging.debug("Wating for job: " + str(job))
        job.join(timeout=10)

    return sum(q) / len(q)


def degrees_of_separation(seps=None):
    """ currently takes a really really long time to finish.
    """
    all_users = _FACE_DATA.data.keys()
    seps = [avg_path_length_for_user(u) for u in all_users]
    return sum(seps) / len(seps)
