import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import user

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

## private functions
def _connection_generator(user_id, limit=10):
    """ Each iteration returns the next level of user_id's conections
        each iteration is O(log(n))
    """
    level = 0
    branch_data = {}
    visited = []

    try:
        branch_data[0] = {(user_id,):[child for child in _get_child_keys(user_id)]}
    except TypeError:
        logging.warn("Connection lookup for empty nodes")
        return

    yield (level, branch_data[0],)

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
                # then check to see if we've already visited this parent node
                if i not in visited:
                    
                    # if we haven't, then find that parent's children
                    try:
                        child_list[i] = [k for k in _get_child_keys(i)]

                    except TypeError:
                        # no more children...
                        pass

                    # finally, mark this parent as visited
                    visited.append(i)

        branch_data[child_level] = child_list
        level += 1
        if len(branch_data[child_level]) is 0:
            break
        else:
            yield (level, branch_data[child_level])


def _all_connections(user_id):
    """
    Generators are great, but sometimes we just want all the data.
    This will build a list that contains all of a user's connections.

    O(n * log(n)) because each iteration of the _connection_generator needs
                  to be iterated over again, inside the list comprehension.
    """
    return [con for con in _connection_generator(user_id)]

def _flatten_connections(connections_data):
    """
    Feed this the entire output from the connections_generator, and this will
    flatten that data structure, and return a basic list.

    O(n)
    """
    return [i[1].keys()[0] for i in connections_data]

def _connections_as_set(user_id):
    """
    O(n^2)
    """
    connections = _all_connections(user_id)
    flat_connections = _flatten_connections(connections)
    return set(flat_connections)

def _get_child_keys(user_id, action='OuttaMyFace'):
    """ returns a list of keys.
        O(1)
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


def _connection_tester(user_id, face):
    """ test to see if a user is connected by checking each level of the tree
        O(log(n)) 
    """
    for cons in _connection_generator(user_id):
        if (face, ) in cons[1].keys():
            return True
    return False


## public functions
def get_face_data(user_id, action=None):
    """ Returns all connection data for a user. This does not detect cycles.

        O(n) or if there are cycles, O(infinit.) 
    """
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
        d = {'user_enabled': user.user_enabled(user_id),
             'face_enabled': user.user_enabled(face),
             'face_InMyFace': is_in_my_face(user_id, face),
             'path_to_user_from_face': None,
             'user_InMyFace': is_outta_my_face(user_id, face),
             'path_to_face_from_user':None,
            }

        if d['face_InMyFace']:
            d['path_to_user_from_face'] = find_path(user_id, face)
            d['path_to_face_from_user'] = find_path(face, user_id)

        return d

    try:
        return data()
    except:
        return False



def face_space(user_a, user_b):
    """ with which members are both user_a and user_b indirectly connected?
        ie, who sees posts from both users_a and users_b
    """
    return connection_intersect(user_a, user_b)

def connection_intersect(user_a, user_b):
    user_a_set = _connections_as_set(user_a)
    user_b_set = _connections_as_set(user_b)

    return user_a_set.intersection(user_b_set)

def is_outta_my_face(user_id, face):
    """ O(n^2)
    """
    return _connection_tester(user_id, face)

def is_in_my_face(user_id, face):
    """ O(n^2)
    """
    return _connection_tester(face, user_id)

def find_path(user_id, face, path=None, find_shortest=False):

    if type(user_id) is not tuple:
        user_id = (user_id,)
    if type(face) is not tuple:
        face = (face,)

    if path is None:
        # fresh path, no data yet...
        path = []
    else:
        # adding the current user_id to the path
        path = path + [user_id]

    if user_id == face:
        # through recursion, we've found our endpoint. 
        # return the full path
        return path

    child_keys = _get_child_keys(user_id)
    shortest_path = None

    if not child_keys:
        # if we dont have a node named 'user_id' return None
        return None

    for child in child_keys:
        if child not in path:
            logging.debug("searching path for: " + str(child))

            newpath = find_path(child, face, path)

            if newpath and not find_shortest:
                # we don't care to find the shortest path, we just want the
                # fastest results.
                return newpath

            elif newpath and find_shortest:
                # we need to know what the shortest path between two nodes is
                # so this will take longer to test.
                if not shortest_path or len(newpath) < len(shortest_path):
                    shortest_path = newpath


    return shortest_path


