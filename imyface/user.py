#import hashlib
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import connect

from data_layer.user_data import UserData
_USER_DATA = UserData()

class UserExists(Exception):
    pass

## private functions
def _new_user(last_name,
              first_name,
              user_id,
              password,
              save=False):
    """ Insert user into data dict.
        Each member of the dict must be unique, as identified by the key.

        O(1)
    """
    # add new row to user_data db
    d = {'data': (first_name, last_name, password),'enabled': True}
    _USER_DATA.insert(user_id, d)

    # create an empty node in the face_data db
    connect.init_user(user_id)


## public functions 
def is_existing_user(user_id):
    """ Check to see if a user exists in the data dict

        O(1)
    """
    return _USER_DATA.data.has_key((user_id,))

def enroll(first_name, 
           last_name,
           user_id,
           password):
    """ Allows a user to provide basic information

        O(1) 
        ( however this may be as slow as O(n) if there are a lot of 
        hash collisions on dict insert )
    """
    if not is_existing_user(user_id):
        _new_user(last_name, first_name, user_id, password)
    else:
        raise UserExists("Found existing user %s in db" % (user_id))

def user_enabled(user_id):
    """ Check if a user is enabled
        O(1)
    """
    return _USER_DATA.data.get((user_id,))['enabled']

def disable_user(user_id):
    """ Disable a user
        O(1)
    """
    _USER_DATA.update_subkey(user_id, 'enabled', False)

def enable_user(user_id):
    """ Enable a user
        O(1)
    """ 
    _USER_DATA.update_subkey(user_id, 'enabled', True)

def get_user(user_id):
    """ Get user data
        O(1)
    """
    u = _USER_DATA.data.get((user_id,), None)
    if u is None:
        return
    user_data = u['data']
    return user_data

def get_user_count():
    """ dict keeps track of how many elements it contains
        O(1)
    """
    return len(_USER_DATA.data)

def enroll_list(users_list):
    """ Enroll all users in a list
        O(n)
    """
    users_loaded = 0
    for r in users_list:
        enroll(r[0], r[1], r[2], r[3])
        users_loaded += 1
    return users_loaded


