from nose.tools import *
import cPickle as pickle

from test_config import FACE_DATA_FILE
#import user_test

from imyface import actions, user, connect

from imyface.data_layer.user_data import UserData
from imyface.data_layer.face_data import FaceData
_USER_DATA = UserData()
_FACE_DATA = FaceData()

from tests import user_test

CONNECTIONS_LOADED = 0
ROWS = []

#@with_setup(setup=user_test.setup,teardown=user_test.tear_down)
def load_connections():
    global CONNECTIONS_LOADED
    global ROWS

#    _USER_DATA.reset()
#    _FACE_DATA.reset()

    fp = open(FACE_DATA_FILE, 'rb')
    connections_list = pickle.load(fp)
    CONNECTIONS_LOADED = connect.connect_list(connections_list)

    for r in range(0, 10):
        # load the first 10 rows into a global for testing
        ROWS.append(connections_list[r])

def load_users():
    user_test.load_users()
    load_connections()

def teardown():
    global CONNECTIONS_LOADED
    global FIRST_ROW
    CONNECTIONS_LOADED = 0 
    FIRST_ROW = None
#    user_test.tear_down()
    _USER_DATA.reset()
    _FACE_DATA.reset()

@with_setup(setup=load_users, teardown=teardown)
def test_direct_connection():
    uid1 = ROWS[0][2]
    uid2 = ROWS[1][2]
    connect.outta_my_face(uid1, uid2)
    assert_true(actions.is_outta_my_face(uid1, uid2))

@with_setup(setup=load_users, teardown=teardown)
def test_second_connection():
    """ test connected, not connected users
    """

    # these users are connected to uid1
    uid1 = ROWS[0][2]
    uid2 = ROWS[1][2]
    uid3 = ROWS[2][2]
    uid4 = ROWS[3][2]

    assert_true(actions.is_outta_my_face(uid1, uid1))

    connect.outta_my_face(uid1, uid2)
    assert_true(actions.is_outta_my_face(uid1, uid2))

    connect.outta_my_face(uid2, uid3)
    assert_true(actions.is_outta_my_face(uid2, uid3))
    assert_true(actions.is_outta_my_face(uid1, uid3))

    connect.outta_my_face(uid3, uid4)
    assert_true(actions.is_outta_my_face(uid3, uid4))
    assert_true(actions.is_outta_my_face(uid2, uid4))
    assert_true(actions.is_outta_my_face(uid1, uid4))


@with_setup(setup=load_users, teardown=teardown)
def test_bi_direction_out():
    uid1 = ROWS[0][2]

    # these users are not connected to uid1
    uid6 = 'crap'
    user.enroll(uid6,uid6,uid6,uid6)
    uid7 = 'crap2'
    user.enroll(uid7,uid7,uid7,uid7)

    connect.outta_my_face(uid6,uid7)
    assert_true(actions.is_outta_my_face(uid6, uid7))
    assert_true(actions.is_in_my_face(uid7, uid6))

    # inverse test
    assert_false(actions.is_outta_my_face(uid7, uid6))
    assert_false(actions.is_in_my_face(uid6, uid7))

    # finally, test to make sure these users aren't connected to uid1
    assert_false(actions.is_outta_my_face(uid1, uid6))
    assert_false(actions.is_outta_my_face(uid1, uid7))
    assert_false(actions.is_in_my_face(uid1, uid6))
    assert_false(actions.is_in_my_face(uid1, uid7))

@with_setup(setup=load_users, teardown=teardown)
def test_bi_direction_in():
    uid1 = ROWS[0][2]

    # these users are not connected to uid1
    uid6 = 'crap'
    user.enroll(uid6,uid6,uid6,uid6)
    uid7 = 'crap2'
    user.enroll(uid7,uid7,uid7,uid7)

    connect.in_my_face(uid6, uid7)
    assert_false(actions.is_outta_my_face(uid6, uid7))
    assert_false(actions.is_in_my_face(uid7, uid6))

    # inverse test
    assert_true(actions.is_outta_my_face(uid7, uid6))
    assert_true(actions.is_in_my_face(uid6, uid7))

    # finally, test to make sure these users aren't connected to uid1
    assert_false(actions.is_outta_my_face(uid1, uid6))
    assert_false(actions.is_outta_my_face(uid1, uid7))
    assert_false(actions.is_in_my_face(uid1, uid6))
    assert_false(actions.is_in_my_face(uid1, uid7))

@with_setup(setup=load_users, teardown=teardown)
def test_bi_direction_in_and_out():
    uid1 = ROWS[0][2]

    # these users are not connected to uid1
    uid6 = 'crap'
    user.enroll(uid6,uid6,uid6,uid6)
    uid7 = 'crap2'
    user.enroll(uid7,uid7,uid7,uid7)

    connect.in_my_face(uid6, uid7)
    connect.outta_my_face(uid6, uid7)
    assert_true(actions.is_outta_my_face(uid6, uid7))
    assert_true(actions.is_in_my_face(uid7, uid6))

    # inverse test
    assert_true(actions.is_outta_my_face(uid7, uid6))
    assert_true(actions.is_in_my_face(uid6, uid7))

    # finally, test to make sure these users aren't connected to uid1
    assert_false(actions.is_outta_my_face(uid1, uid6))
    assert_false(actions.is_outta_my_face(uid1, uid7))
    assert_false(actions.is_in_my_face(uid1, uid6))
    assert_false(actions.is_in_my_face(uid1, uid7))

@with_setup(teardown=teardown)
def test_flat_list():
    u1 = 'uid1'
    u2 = 'uid2'
    u3 = 'uid3'
    u4 = 'uid4'
    mr_popular = 'uid5'
    user.enroll(u1, u1, u1, u1)
    user.enroll(u2, u2, u2, u2)
    user.enroll(u3, u3, u3, u3)
    user.enroll(u4, u4, u4, u4)
    user.enroll(mr_popular, mr_popular, mr_popular, mr_popular)

    connect.outta_my_face(u1, u2)
    connect.outta_my_face(u3, u4)
    connect.outta_my_face(u2, mr_popular)
    connect.outta_my_face(u4, mr_popular)

    users_set1 = actions._all_connections(u1)
    users_set1_flat = actions._flatten_connections(users_set1)
    print users_set1_flat

    users_set2 = actions._all_connections(u3)
    users_set2_flat = actions._flatten_connections(users_set2)
    print users_set2_flat

    # first connection is always the user we started searching at
    assert_equal(users_set1[0][2].keys(), [(u1,)] )
    assert_equal(users_set2[0][2].keys(), [(u3,)] )

    # our user_set data should be a list of users, with order
    assert_equal(users_set1_flat, [(u1,), (u2,), (mr_popular,)] )
    assert_equal(users_set2_flat, [(u3,), (u4,), (mr_popular,)] )

    intersect = {(mr_popular,)}

    print actions.face_space(u1, u3)

    #mr_popular should be connected to everyone
    assert_equal(actions.face_space(u1, u3), intersect)
    assert_equal(actions.face_space(u3, u1), intersect)
    assert_equal(actions.face_space(u2, u4), intersect)
    assert_equal(actions.face_space(u4, u2), intersect)

