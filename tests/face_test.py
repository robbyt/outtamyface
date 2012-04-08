from nose.tools import *
import cPickle as pickle

import user_test
from imyface import user, actions

FACE_DATA_FILE = 'demo_data/data1_connections__small-no-cycles.dat.pickle'

from imyface.data_layer import user_data, face_data
_USER_DATA = user_data.USER_DATA
_FACE_DATA = face_data.FACE_DATA

CONNECTIONS_LOADED = 0
FIRST_ROW = None

#@with_setup(setup=user_test.setup,teardown=user_test.tear_down)
def _setup():
    global CONNECTIONS_LOADED
    global FIRST_ROW

    user_test.tear_down()
    user_test.setup()

    print _USER_DATA
#    print _FACE_DATA

    fp = open(FACE_DATA_FILE, 'rb')
    connections_list = pickle.load(fp)
    for u in connections_list:
        actions.connect(u[0], u[1], u[2])
        CONNECTIONS_LOADED += 1

    FIRST_ROW = connections_list[0]

def _teardown():
    global CONNECTIONS_LOADED
    global FIRST_ROW
    CONNECTIONS_LOADED = 0 
    FIRST_ROW = None
    user_test.tear_down()

@with_setup(setup=_setup,teardown=_teardown)
def test_connection():
    assert_true(True)
