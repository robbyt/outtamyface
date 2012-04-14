import logging
from collections import deque
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from data_layer.face_data import FACE_DATA as _FACE_DATA


class ConnectionProblem(Exception):
    pass


## private functions
def _get_child_keys(user_id, action='OuttaMyFace'):
    """ returns a list of keys
    """
    if type(user_id) is tuple:
        user_id = user_id[0]

    try:
        d = _FACE_DATA[(user_id,)][(action,)].keys()
        if d:
            return d
        else:
#            assert(False)
            return ['']
    except KeyError:
        return

def _child_keys_generator(user_id, action='OuttaMyFace'):
    """ user_id keys as generator
    """
#    visited = []
    try:

        if type(user_id) is str:
            connections = _FACE_DATA[(user_id,)][(action,)].keys()
            for row in set(connections):
                yield row

        elif type(user_id) is list:
            for row in user_id:
                connections = _FACE_DATA[(row,)][(action,)].keys()
                for k in set(connections):
                    yield k

    except KeyError:
        logging.error("Key not found in _ckg: " + str(user_id))
        return


## public functions
def init_user(user_id):
    return _FACE_DATA.setdefault((user_id,), {})

def connect(user1, action, user2):
    """ docs
    """

    # create an empty branch, or retrieve the existing
    u1_tree_out = _FACE_DATA[(user1,)].setdefault(('OuttaMyFace',), {})
    u1_tree_in = _FACE_DATA[(user1,)].setdefault(('InMyFace',), {})
    # do the same for u2
    u2_tree_out = _FACE_DATA[(user2,)].setdefault(('OuttaMyFace',), {})
    u2_tree_in = _FACE_DATA[(user2,)].setdefault(('InMyFace',), {})

    d = {'OuttaMyFace':{
            'u1_tree': u1_tree_out,
            'u2_tree': u2_tree_out},
         'InMyFace':{
            'u1_tree': u1_tree_in,
            'u2_tree': u2_tree_in},
        }


    try:
        if d[action]['u2_tree'] is None:

            # if none, then that means u2_tree is empty, so do init
            _FACE_DATA[(user1,)][(action,)][(user2,)] = {}

        else:

            # else, u2_tree has some data, so update it with a new key
            _FACE_DATA[(user1,)][(action,)][(user2,)] = _FACE_DATA[(user2,)][(action,)]

    except KeyError:
        raise ConnectionProblem
#        logging.error("Problem adding connection")

def disconnect(user1, action, user2):
    try:
        del(_FACE_DATA[(user1,)][(action,)][(user2,)])
    except KeyError:
        logging.warn("Problem in {1} tree, cannot remove {1} / {2}".format(user1, action, user2))
        return False

def get_face_data(user_id, action=None):
    try:
        if action is None:
            return _FACE_DATA[(user_id,)]
        else:
            return _FACE_DATA[(user_id,)][(action,)]
    except KeyError:
            logging.warn("Problem finding face_data for: {0} / {1}".format(user_id, action))
            return False

def outta_my_face(user, face):
    """ when a user asks another member ('the face') to be "outta my face"
        ie, "connected" (if 'the face' accepts) then posts to the user's page
        will broadcast to "the face" page and posted there too. 

        Everyone "outta" the face's page, will be asked if they want to be 
        "outta" the user's page too. 

        analogous to asking the Face to "permanent retweet" user's posts, 
        and additionally broadcasting your posts to everyone who also accepts

        me == outta ==> tom
        me == outta ==> [tom's contacts: 'larry', 'billy']

        when user sends an outta_my_Face to a face1,
        and a user posts to user's page,
        then posts will be sent to the face1 page also.

        additionally, all faces that are outta on face1 will receive posts
        from user.
    """
    connect(user, 'OuttaMyFace', face)

def in_my_face(user, face):
    """ the user asks another member to be "in my face", ie, have updates from
        the Face's page sent to the user's page. Thsi works like an outta, but
        in reverse.

        analogous to a following someone on twitter, and broadcasting to
        everyone you follow that you are following someone new.

        me <== in request == tom
        < tom accepts >
        tom == outta request ==> [my contacts]
    """
    connect(user, 'InMyFace', face)

def faced_up(user, face):
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
    d = {'face_enabled': user.user_enabled(face),
         'face_InMyFace': None,
         'path_to_user_from_face': None,
         'user_InMyFace': None,
         'path_to_face_from_user':None
        }
    try:
        return d
    except:
        return False

def face_space(user_a, user_b):
    """ with which members are both user_a and user_b indirectly connected?
        ie, who sees posts from both users_a and users_b
    """
    pass

def connect_list(users_list):
    """ Enroll all users in a list
        O(n)
    """
    connections_loaded = 0
    for r in users_list:
        connect(r[0], r[1], r[2])
        connections_loaded += 1

    return connections_loaded

def connection_generator(user_id, limit=10, action='OuttaMyFace'):
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
#        logging.debug("Parent level: " + str(parent_level))

        # increment the level, to track our child level
        child_level = level + 1
#        logging.debug("Child level: " + str(child_level))

        # empty dict that will store our results for this level
        child_list = {}

        # for every parent in our previous branch level
        for parent, child in branch_data[parent_level].iteritems():

            for i in child:
#                logging.debug("Lookup for: " + str(i) )
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
                        child_list[i].append(('',))

                # finally, mark this parent as visited
                visited.append(i)

        branch_data[child_level] = child_list
        level += 1
        if len(branch_data[child_level]) is 0:
            break
        else:
            yield (action, level, branch_data[child_level])


def is_outta(user_id, face, action='OuttaMyFace'):
    """ O(n^2)
    """
    for cons in connection_generator(user_id=user_id, action=action):
        if (face, ) in cons[2].keys():
            #logging.debug("Found %s in %s" % ((face), cons[2].keys()))
            return True
        #else:
            #logging.debug("Coult not find %s in %s" % (face, cons[2].keys()))
    return False



