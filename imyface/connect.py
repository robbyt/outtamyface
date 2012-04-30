import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from data_layer.face_data import FaceData
_FACE_DATA = FaceData()

class ConnectionProblem(Exception):
    pass

## public functions
def init_user(user_id):
    return _FACE_DATA.init_user(user_id)

def _connect(user1, user2):
    """ docs
    """

    # create an empty branch, or retrieve the existing
    u1_tree_out = _FACE_DATA.data[(user1,)].setdefault(('OuttaMyFace',), {})
    # do the same for u2
    u2_tree_out = _FACE_DATA.data[(user2,)].setdefault(('OuttaMyFace',), {})


    try:
        if u2_tree_out is None:
            # if none, then that means u2_tree is empty, so do init
            _FACE_DATA.data[(user1,)][('OuttaMyFace',)][(user2,)] = {}

        else:
            # else, u2_tree has some data, so update it with a new key
            _FACE_DATA.data[(user1,)][('OuttaMyFace',)][(user2,)] = _FACE_DATA.data[(user2,)][('OuttaMyFace',)]

    except KeyError:
        raise ConnectionProblem
#        logging.error("Problem adding connection")

def disconnect(user1, action, user2):
    try:
        del(_FACE_DATA.data[(user1,)][(action,)][(user2,)])
        return True
    except KeyError:
        logging.warn("Problem in {1} tree, cannot remove {1} / {2}".format(user1, action, user2))
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
    _connect(user, face)
#    _connect(face, 'InMyFace', user)

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
#    _connect(user, 'InMyFace', face)
    _connect(face, user)

def connect_list(users_list):
    """ Enroll all users in a list
        O(n)
    """
    connections_loaded = 0
    d = {'OuttaMyFace': outta_my_face,
         'InMyFace': in_my_face}

    for r in users_list:
        user_id = r[0]
        action = r[1]
        face = r[2]

        d[action](user_id, face)
        connections_loaded += 1

    return connections_loaded


