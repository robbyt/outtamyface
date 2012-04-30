OuttaMyFace
=============
This is an example of an in-memory graph database.


Working With This Thing
-----------------------

### Load up the demo data:

```python

import cPickle as pickle
from imyface import user, actions, connect

cons_file = 'demo_data/data4_connections__larger.dat.pickle'
users_file = 'demo_data/data4_faces__larger.dat.pickle'

fp_cons = open(cons_file)
fp_users = open(users_file)
users_list = pickle.load(fp_users)
cons_list = pickle.load(fp_cons)

user.enroll_list(users_list)
connect.connect_list(cons_list)
```

### Get a list of all users:
```python
print user.get_all_users()
# sorted list of users:
print user.get_all_users(sort_list=True)
```

