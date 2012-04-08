#import hashlib
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from data_layer import user_data, face_data
_USER_DATA = user_data.USER_DATA
_FACE_DATA = face_data.FACE_DATA

class UserExists(Exception):
    pass

## private functions
def _get_user(user_id):
    return _USER_DATA.get(user_id)

def _new_user(last_name,
              first_name,
              user_id,
              password,
              save=False):
    """ Insert user into data dict.
        Each member of the dict must be unique, as identified by the key.
    """
    # add new row to user_data db
    _USER_DATA[user_id] = (first_name, last_name, password)
#    logging.debug("Added new user %s to user_data" % (user_id))

    # create an empty node in the face_data db
    _FACE_DATA.setdefault(user_id, {})
#    logging.debug("Added new user %s to face_data" % (user_id))

    if save:
        user_data.save()

## public functions 
def is_existing_user(user_id):
    """Check to see if a user exists in the data dict
    """
    return _USER_DATA.has_key(user_id)

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

