#import hashlib
import itertools
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

#from data_layer.user_data import USER_DATA as _USER_DATA
from data_layer.face_data import FACE_DATA as _FACE_DATA

## private functions
def _get_child_keys(user_id, action='OuttaMyFace'):
    """ returns a list of keys
    """
    try:
        d = _FACE_DATA[(user_id,)][(action,)].keys()
        if d:
            return d
        else:
            return ['']
    except KeyError:
        return

def _child_keys_gennerator(user_id, action='OuttaMyFace'):
    """ returns a list of keys
    """
    try:
        d = _FACE_DATA[(user_id,)][(action,)].keys()
        for k in d:
            yield k
#        if d:
#            return d
#        else:
#            return 'STOP'
    except KeyError:
        return



## public functions
def init_user(user_id):
    _FACE_DATA.setdefault((user_id,), {})

def connect(user1, action, user2):
    """
    """

    # create an empty branch, or retrieve the existing
    u1_tree = _FACE_DATA[(user1,)].setdefault((action,), {})

    # do the same for u2
    u2_tree = _FACE_DATA[(user2,)].setdefault((action,), {})

    if u2_tree is None:
        _FACE_DATA[(user1,)][(action,)][(user2,)] = {}
    else:
        _FACE_DATA[(user1,)][(action,)][(user2,)] = _FACE_DATA[(user2,)][(action,)]

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
    """
    connections_loaded = 0
    for r in users_list:
        connect(r[0], r[1], r[2])
        connections_loaded += 1

    return connections_loaded

def connection_gennerator(user_id, limit=10, action='OuttaMyFace'):
    level = 0
    branch_data = {}

    branch_data[0] = _get_child_keys(user_id)
    yield (level, branch_data[0])

    while level <= limit:
        parent_level = level
        logging.debug("Parent level: " + str(parent_level))
        child_level = level + 1
        logging.debug("Child level: " + str(child_level))
#        branch_data[child_level] = []
#        for f in branch_data[parent_level]:
#            branch_data[child_level].append(_get_child_keys(f[0]))
        l = [_get_child_keys(f[0]) for f in branch_data[parent_level] if f is not ""]
#        logging.debug("List from listcomp: " + str(l))
        l_flat = sum(l, [])
#        logging.debug("List of l_flat: " + str(l_flat))
        branch_data[child_level] = l_flat
        level +=1
        if branch_data[child_level] == ['']:
            break
        else:
            yield (level, branch_data[child_level])

def is_outta(user_id, face, action='OuttaMyFace'):
    levels = 0
    path = []
    
    def face_finder(u, f):
        return _FACE_DATA[(u,)][('OuttaMyFace',)].has_key((f,))

    try:
        if face_finder(user_id, face):
            return True
        else:
            for i in _FACE_DATA[(user_id,)][('OuttaMyFace',)].iteritems():
                #TBD
                assert(False)
                i
                levels += 1
            
    except KeyError:
            logging.warn("Problem finding outta status for: {0} / {1}".format(user_id, face))
            return False



