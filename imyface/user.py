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
    """
    # add new row to user_data db
    d = {'data': (first_name, last_name, password),'enabled': True}
    _USER_DATA.insert(user_id, d)

#    logging.debug("Added new user %s to user_data" % (user_id))
    # create an empty node in the face_data db
    connect.init_user(user_id)
#    logging.debug("Added new user %s to face_data" % (user_id))

#    if save:
#        user_data.save()

## public functions 
def is_existing_user(user_id):
    """Check to see if a user exists in the data dict
    """
    return _USER_DATA.data.has_key((user_id,))

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

def user_enabled(user_id):
    return _USER_DATA.data.get((user_id,))['enabled']

def disable_user(user_id):
    _USER_DATA.data.get((user_id,))['enabled'] = False

def enable_user(user_id):
    _USER_DATA.data.get((user_id,))['enabled'] = True

def get_user(user_id):
    return _USER_DATA.data.get((user_id,))['data']

def get_user_count():
    return len(_USER_DATA.data)

def enroll_list(users_list):
    """ Enroll all users in a list
    """
    users_loaded = 0
    for r in users_list:
        enroll(r[0], r[1], r[2], r[3])
        users_loaded += 1
    return users_loaded


