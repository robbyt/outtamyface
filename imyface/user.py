#import hashlib
from imyface_data import USER_DATA as _USER_DATA

class UserExists(Exception):
    pass

def is_existing_user(user_id):
    """Check to see if a user exists in the data dict
        
    """
    return _USER_DATA.has_key(user_id)

def _get_user(user_id):
    return _USER_DATA.get(user_id)

def _new_user(last_name,
              first_name,
              user_id,
              password):
    """Insert user into data dict
    """
#    user_data['user_id'] = {'last_name':last_name,
#                            'first_name':first_name,
#                            'password':password,}
    _USER_DATA[user_id] = (first_name, last_name, password)

def enroll(first_name, 
           last_name,
           user_id,
           password):
    """ Allows a user to provide basic information
    """
    if not is_existing_user(user_id):
        _new_user(last_name, first_name, user_id, password)
    else:
        raise UserExists("Found existing user %s in db" % (user_id))

def get_user(user_id):
    return _get_user(user_id)

def get_user_count():
    return len(_USER_DATA)

def outta_my_face():
    """ when a user asks another member ('the face') to be "outta my face"
        ie, "connected" (if 'the face' accepts) then posts to the user's page
        will broadcast to "the face" page and posted there too. 

        Everyone "outta" the face's page, will be asked if they want to be 
        "outta" the user's page too. 

        analogous to a following someone on twitter, and broadcasting to
        everyone you follow that you are following someone new.

        me == outta request ==> tom
        < tom accepts>
        me == connected ==> tom
        me == outta request ==> [tom's contacts: 'larry', 'billy']
        me == outta request ==> larry ==> [larry's contacts] 
        me == outta request ==> billy ...

    """
    pass

def in_my_face():
    """ the user asks another member to be "in my face", ie, have updates from
        the Face's page sent to the user's page. Thsi works like an outta, but
        in reverse.

        analogous to a "permanent retweet", and additionally broadcasting to
        everyone on twitter that you are retweeting someone new

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

