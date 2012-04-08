from nose.tools import *
from imyface import user

def test_enroll():
    fn = 'John'
    ln = 'Smith'
    uid = 'jsmith'
    pw = 'pass'

    user.enroll(fn, ln, uid, pw)
    u = user.get_user(uid)
    assert_equal(u, (fn, ln, pw))

