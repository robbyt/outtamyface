import logging
from collections import deque
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import user

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

## private functions
def _connection_generator(user_id, limit=10, action='OuttaMyFace'):
    """ O(n)
    """
    level = 0
    branch_data = {}
    visited = []

    try:
        branch_data[0] = {(user_id,):[child for child in _get_child_keys(user_id)]}
    except TypeError:
        logging.warn("Connection lookup for empty nodes")
        return

    yield (action, level, branch_data[0],)

    while level < limit:
        # capture the current level of the tree
        parent_level = level

        # increment the level, to track our child level
        child_level = level + 1

        # empty dict that will store our results for this level
        child_list = {}

        # for every parent in our previous branch level
        for parent, child in branch_data[parent_level].iteritems():

            for i in child:
                # create an empty list, use parent as key
                child_list[i] = []

                # then check to see if we've already visited this parent node
                if i not in visited:
                    
                    # if we haven't, then find that parent's children
                    try:
                        for next_child in _get_child_keys(i):
    
                            # and add each child to the child_list results
                            child_list[i].append(next_child)

                    except TypeError:
                        pass
                        #child_list[i].append(('',))

                # finally, mark this parent as visited
                visited.append(i)

        branch_data[child_level] = child_list
        level += 1
        if len(branch_data[child_level]) is 0:
            break
        else:
            yield (action, level, branch_data[child_level])


def _get_child_keys(user_id, action='OuttaMyFace'):
    """ returns a list of keys
    """
    if type(user_id) is tuple:
        user_id = user_id[0]

    try:
        d = _FACE_DATA.data[(user_id,)][(action,)].keys()
        if d:
            return d
        else:
            return ['']
    except KeyError:
        return

def _child_keys_generator(user_id, action='OuttaMyFace'):
    """ user_id keys as generator
    """
    try:
        if type(user_id) is str:
            connections = _FACE_DATA.data[(user_id,)][(action,)].keys()
            for row in set(connections):
                yield row
        elif type(user_id) is list:
            for row in user_id:
                connections = _FACE_DATA.data[(row,)][(action,)].keys()
                for k in set(connections):
                    yield k

    except KeyError:
        logging.error("Key not found in _ckg: " + str(user_id))
        return

def _connection_tester(user_id, face):
    """ test to see if a user is connected by checking each level of the tree
        O(n^2)
    """
    for cons in _connection_generator(user_id=user_id, action='OuttaMyFace'):
        if (face, ) in cons[2].keys():
            return True
    return False


def _connection_path_finder(user_id, face):
    pass


## public functions
def get_face_data(user_id, action=None):
    try:
        if action is None:
            return _FACE_DATA.data[(user_id,)]
        else:
            return _FACE_DATA.data[(user_id,)][(action,)]
    except KeyError:
            logging.warn("Problem finding face_data for: {0} / {1}".format(user_id, action))
            return

def faced_up(user_id, face):
    """ Test to see if a face is connected. will posts to the user's page be
        displayed on the face's page. Tests connection.

        user = user that is testing 
        face = target face, that we are testing membership for

        - Whether the Face is currently a community member

        - Whether the Face is InMyFace with respect to the user. So for 
          example, if B is "OuttaMyFace" with respect to A, and C is 
          "Outta" B, then updates to A will automatically be posted on B, 
          and then automatically posted on C.

        - The sequence(s) of Faces through which the user's posts will reach
          the Face?

        - Whether the Face is InYourFace with respect to the user.

        - The sequence(s) of Faces through which the Face's posts will reach
          the user.

    """
    def data():
        d = {'face_enabled': user.user_enabled(face),
             'face_InMyFace': is_in_my_face(user_id, face),
             'path_to_user_from_face': None,
             'user_InMyFace': is_outta_my_face(user_id, face),
             'path_to_face_from_user':None,
            }
        return d

    try:
        return data()
    except:
        return False

def face_space(user_a, user_b):
    """ with which members are both user_a and user_b indirectly connected?
        ie, who sees posts from both users_a and users_b
    """
    pass

def is_outta_my_face(user_id, face):
    """ O(n^2)
    """
    return _connection_tester(user_id, face)

def is_in_my_face(user_id, face):
    """ O(n^2)
    """
    return _connection_tester(face, user_id)

