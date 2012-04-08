#import hashlib
from data_layer import user
from data_layer import face

_USER_DATA = user.USER_DATA
_FACE_DATA = face.FACE_DATA

def connect(user1, action, user2):
    
    pass

def outta_my_face(user, face):
    """ when a user asks another member ('the face') to be "outta my face"
        ie, "connected" (if 'the face' accepts) then posts to the user's page
        will broadcast to "the face" page and posted there too. 

        Everyone "outta" the face's page, will be asked if they want to be 
        "outta" the user's page too. 

        analogous to asking the Face to "permanent retweet" user's posts, 
        and additionally broadcasting your posts to everyone who also accepts

        me == outta request ==> tom
        < tom accepts>
        me == connected ==> tom
        me == outta request ==> [tom's contacts: 'larry', 'billy']
        me == outta request ==> larry ==> [larry's contacts] 
        me == outta request ==> billy ...

    """
    _connect(user, 'OuttaMyFace', face)

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

