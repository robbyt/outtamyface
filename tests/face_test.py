from nose.tools import *
import cPickle as pickle

from test_config import FACE_DATA_FILE
import user_test

from imyface import actions


from imyface.data_layer import user_data, face_data
_USER_DATA = user_data.USER_DATA
_FACE_DATA = face_data.FACE_DATA

CONNECTIONS_LOADED = 0
ROWS = []

#@with_setup(setup=user_test.setup,teardown=user_test.tear_down)
def _setup():
    global CONNECTIONS_LOADED
    global ROWS

    user_test.tear_down()
    user_test.setup()

    print _USER_DATA
#    print _FACE_DATA

    fp = open(FACE_DATA_FILE, 'rb')
    connections_list = pickle.load(fp)
    CONNECTIONS_LOADED = actions.connect_list(connections_list)

    for r in range(0, 10):
        # load the first 10 rows into a global for testing
        ROWS.append(connections_list[r])

    return

def _teardown():
    global CONNECTIONS_LOADED
    global FIRST_ROW
    CONNECTIONS_LOADED = 0 
    FIRST_ROW = None
    user_test.tear_down()

@with_setup(setup=_setup,teardown=_teardown)
def test_simple_connection():
    uid1 = ROWS[0][2]
    uid2 = ROWS[1][2]
    actions.outta_my_face(uid1, uid2)
    assert_true(actions.is_outta(uid1, uid2))

