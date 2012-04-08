#import hashlib
from data_layer import user as data
_USER_DATA = data.USER_DATA

class UserExists(Exception):
    pass

## private functions
def _get_user(user_id):
    return _USER_DATA.get(user_id)

def _new_user(last_name,
              first_name,
              user_id,
              password,
              save=True):
    """ Insert user into data dict.
        Each member of the dict must be unique, as identified by the key.
    """
    _USER_DATA[user_id] = (first_name, last_name, password)
    if save:
        data.save()

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

