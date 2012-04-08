#import hashlib
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

#from data_layer.user_data import USER_DATA as _USER_DATA
from data_layer.face_data import FACE_DATA as _FACE_DATA


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
        
def get_face_data(user_id):
    try:
        return _FACE_DATA[(user_id,)]
    except KeyError:
        logging.warn("Problem finding face_data for: " + user_id)
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

def in_my_face():
    """ the user asks another member to be "in my face", ie, have updates from
        the Face's page sent to the user's page. Thsi works like an outta, but
        in reverse.

        analogous to a following someone on twitter, and broadcasting to
        everyone you follow that you are following someone new.

        me <== in request == tom
        < tom accepts >
        tom == outta request ==> [my contacts]
    """
    pass

def faced_up(user, face):
    """ Test to see if a face is connected. will posts to the user's page be
        displayed on the face's page. Tests connection.

        user = user that is testing 
        face = target face, that we are testing membership for
    """
    pass


def face_space(user_a, user_b):
    """ with which members are both user_a and user_b indirectly connected?
        ie, who sees posts from both users_a and users_b
    """
    pass


def connect_list(users_list):
    """ Enroll all users in a list
    """
    for r in users_list:
        connect(r[0], r[1], r[2])

