from nose.tools import *
from imyface import user
import cPickle as pickle

USER_DATA_FILE = 'demo_data/data1_faces__small-no-cycles.dat.pickle'

def _setup():
    users_loaded = 0

    fp = open(USER_DATA_FILE, 'rb')
    user_list = pickle.load(fp)
    for u in user_list:
        user.enroll(u[0], u[1], u[2], u[3])
        users_loaded += 1

    first_row = user_list[0]

    return (users_loaded, first_row)

def tear_down():
    user._USER_DATA = {}

def test_enroll_load():
    """ Loads some users data into our db from USER_DATA_FILE, which returns 
        #rows and 1st row. Then count the number of rows in our db, and check
        the first row to make sure it loaded correctly.
    """
    setup_data = _setup()
    users_loaded = setup_data[0]

    users_in_db = user.get_user_count()
    assert_equal(users_in_db, users_loaded)

    t_user = setup_data[1]
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

def test_no_dupes():
    """ Make sure that redundant users cannot be enrolled
    """
    with assert_raises(user.UserExists):
        user.enroll('John', 'Smith', 'jsmith', 'pass')

def test_is_existing():
    assert_true(user.is_existing_user('jsmith'))
    tear_down()


