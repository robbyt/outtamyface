from nose.tools import *
from imyface import user

from imyface.data_layer import user_data, face_data

import cPickle as pickle

USER_DATA_FILE = 'demo_data/data1_faces__small-no-cycles.dat.pickle'

USERS_LOADED = 0
FIRST_ROW = None

def setup():
    global USERS_LOADED
    global FIRST_ROW

    fp = open(USER_DATA_FILE, 'rb')
    user_list = pickle.load(fp)
    for u in user_list:
        user.enroll(u[0], u[1], u[2], u[3])
        USERS_LOADED += 1

    FIRST_ROW = user_list[0]

def tear_down():
    global USERS_LOADED
    global FIRST_ROW
    USERS_LOADED = 0
    FIRST_ROW = None
    user._USER_DATA = {}

def test_enroll_load():
    """ Loads some users data into our db from USER_DATA_FILE, which returns 
        #rows and 1st row. Then count the number of rows in our db, and check
        the first row to make sure it loaded correctly.
    """
    users_in_db = user.get_user_count()
    assert_equal(users_in_db, USERS_LOADED)

    t_user = FIRST_ROW
    t_fn = t_user[0]
    t_ln = t_user[1]
    t_user_id = t_user[2]
    t_password = t_user[3]

    assert_equal((t_fn, t_ln, t_password), user.get_user(t_user_id)) 

def test_enroll_one():
    fn = 'John'
    ln = 'Smith'
    uid = 'jsmith'
    pw = 'pass'

    user.enroll(fn, ln, uid, pw)
    u = user.get_user(uid)
    assert_equal(u, (fn, ln, pw))

def test_empty_face_data(uid='jsmith'):
    """ We just created this user, so the face_data should be empty.
    """
    assert_equal(face_data.FACE_DATA[uid], {})

def test_no_dupes():
    """ Make sure that dupe users cannot be enrolled
    """
    with assert_raises(user.UserExists):
        user.enroll('John', 'Smith', 'jsmith', 'pass')

def test_is_existing():
    """ the jsmith user should still exist, even though we tried to create a
        duplicate user in the last test.
    """
    assert_true(user.is_existing_user('jsmith'))
    tear_down()

def test_dupe_names():
    """ User accounts should allow duplicate info for everything other than 
        the user_id.
    """
    u1 = {'first_name':'John',
          'last_name':'Smith',
          'user_id':'jsmith',
          'password':'pass'}

    u2 = {'first_name':'John',
          'last_name':'Smith',
          'user_id':'jsmith1',
          'password':'pass'}

    user.enroll(**u1)
    user.enroll(**u2)

    u1_fn = user.get_user(u1['user_id'])[0]
    u1_ln = user.get_user(u1['user_id'])[1]
    u1_pw = user.get_user(u1['user_id'])[2]

    u2_fn = user.get_user(u2['user_id'])[0]
    u2_ln = user.get_user(u2['user_id'])[1]
    u2_pw = user.get_user(u2['user_id'])[2]

    assert_equal(u1_fn, u2_fn)
    assert_equal(u1_ln, u2_ln)
    assert_equal(u1_pw, u2_pw)

    tear_down()
