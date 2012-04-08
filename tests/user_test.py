from nose.tools import *
from imyface import user
import cPickle as pickle

USER_DATA_FILE = 'demo_data/data1_faces__small-no-cycles.dat.pickle'

def tear_down():
    user._USER_DATA = {}

def test_enroll():
    fn = 'John'
    ln = 'Smith'
    uid = 'jsmith'
    pw = 'pass'

    user.enroll(fn, ln, uid, pw)
    u = user.get_user(uid)
    assert_equal(u, (fn, ln, pw))

    tear_down()

def test_enroll_load(data = USER_DATA_FILE):
    """ Loads some users data from 
    """
    users_loaded = 0

    fp = open(data, 'rb')
    user_list = pickle.load(fp)
    for u in user_list:
        user.enroll(u[0], u[1], u[2], u[3])
        users_loaded += 1

    users_in_db = user.get_user_count()
    assert_equal(users_in_db, users_loaded)

    t_user = user_list[1]
    t_fn = t_user[0]
    t_ln = t_user[1]
    t_user_id = t_user[2]
    t_password = t_user[3]

    assert_equal((t_fn, t_ln, t_password), user.get_user(t_user_id)) 

    tear_down()

