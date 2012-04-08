from nose.tools import *
import cPickle as pickle

import user_test
from imyface import user, actions

FACE_DATA_FILE = 'demo_data/data1_connections__small-no-cycles.dat.pickle'

# load users into user_data db
# user_test.setup()

def setup():
    connections_loaded = 0

    fp = open(FACE_DATA_FILE, 'rb')
    connections_list = pickle.load(fp)
    for u in connections_list:
        actions.connect(u[0], u[1], u[2])
        connections_loaded += 1

    first_row = connections_list[0]

    return (connections_loaded, first_row)

def test_connection():
    pass
