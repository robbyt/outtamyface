#import hashlib
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import actions

from data_layer.user_data import USER_DATA as _USER_DATA
#from data_layer.face_data import FACE_DATA as _FACE_DATA

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
    _USER_DATA[(user_id,)] = {'data': (first_name, last_name, password), 
                              'enabled': True}

#    logging.debug("Added new user %s to user_data" % (user_id))

    # create an empty node in the face_data db
    actions.init_user(user_id)
#    logging.debug("Added new user %s to face_data" % (user_id))

#    if save:
#        user_data.save()

## public functions 
def is_existing_user(user_id):
    """Check to see if a user exists in the data dict
    """
    return _USER_DATA.has_key((user_id,))

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
    return _USER_DATA.get((user_id,))['enabled']

def get_user(user_id):
    return _USER_DATA.get((user_id,))['data']

def get_user_count():
    return len(_USER_DATA)

def enroll_list(users_list):
    """ Enroll all users in a list
    """
    for r in users_list:
        enroll(r[0], r[1], r[2], r[3])

