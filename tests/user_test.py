from nose.tools import *
import cPickle as pickle

from test_config import USER_DATA_FILE
from imyface import user, actions

from imyface.data_layer.user_data import UserData
from imyface.data_layer.face_data import FaceData
_USER_DATA = UserData()
_FACE_DATA = FaceData()

USERS_LOADED = 0
FIRST_ROW = None

U1 = {'first_name':'John',
      'last_name':'Smith',
      'user_id':'jsmith',
      'password':'pass'}

U2 = {'first_name':'John',
      'last_name':'Smith',
      'user_id':'jsmith1',
      'password':'pass'}

def load_one_user():
    print _USER_DATA
    print _FACE_DATA
    teardown()
    user.enroll(**U1)

def load_two_users():
    user.enroll(**U1)
    user.enroll(**U2)

def load_users():
    global USERS_LOADED
    global FIRST_ROW

    fp = open(USER_DATA_FILE, 'rb')
    user_list = pickle.load(fp)

    # set the number of users loaded, returned by enroll_list
    USERS_LOADED = user.enroll_list(user_list)

    #grab the first row of test users
    FIRST_ROW = user_list[0]

def teardown():
    print "teardown ran"
    global USERS_LOADED
    global FIRST_ROW
    USERS_LOADED = 0
    FIRST_ROW = None
    _USER_DATA.reset()
    _FACE_DATA.reset()

@with_setup(load_users, teardown)
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

@with_setup(load_one_user, teardown)
def test_enroll_one():
    u = user.get_user(U1['user_id'])
    assert_equal(u, (U1['first_name'], U1['last_name'], U1['password']))

@with_setup(load_one_user, teardown)
def test_empty_face_data():
    """ We just created this user, so the face_data should be empty.
    """
    assert_equal(actions.get_face_data(U1['user_id']), {})

@with_setup(setup=load_one_user, teardown=teardown)
def test_user_enabled():
    uid = U1['user_id']
    assert_true(user.user_enabled(uid))
    user.disable_user(uid)
    assert_false(user.user_enabled(uid))
    user.enable_user(uid)
    assert_true(user.user_enabled(uid))

def test_no_dupes():
    """ Make sure that dupe users cannot be enrolled
    """
    user.enroll('John', 'Smith', 'jsmith', 'pass')
    with assert_raises(user.UserExists):
        user.enroll('John', 'Smith', 'jsmith', 'pass')

@with_setup(teardown=teardown)
def test_is_existing():
    """ the jsmith user should still exist, even though we tried to create a
        duplicate user in the last test.
    """
    assert_true(user.is_existing_user(U1['user_id']))

@with_setup(setup=load_two_users, teardown=teardown)
def test_dupe_names():
    """ User accounts should allow duplicate data  for everything other than 
        the user_id.
        
        fn = first_name
        ln = last_name
        pw = password
    """
    u1_fn = user.get_user(U1['user_id'])[0]
    u1_ln = user.get_user(U1['user_id'])[1]
    u1_pw = user.get_user(U1['user_id'])[2]

    u2_fn = user.get_user(U2['user_id'])[0]
    u2_ln = user.get_user(U2['user_id'])[1]
    u2_pw = user.get_user(U2['user_id'])[2]

    assert_equal(u1_fn, u2_fn)
    assert_equal(u1_ln, u2_ln)
    assert_equal(u1_pw, u2_pw)

@with_setup(setup=load_one_user, teardown=teardown)
def test_get_user_null():
    r = user.get_user('nope')
    assert_true(r is None)
